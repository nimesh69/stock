# accounts/views.py

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# accounts/views.py

from django.middleware.csrf import get_token


class CsrfTokenView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            "csrfToken": get_token(request)
        })
class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        login(request, user)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            },
            status=status.HTTP_201_CREATED,
        )
        
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        })
        
from rest_framework.permissions import IsAuthenticated


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }
        })
        
class LogoutView(APIView):

    def post(self, request):
        logout(request)

        return Response({
            "detail": "Logged out successfully."
        })