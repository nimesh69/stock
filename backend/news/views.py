from rest_framework import generics
from .models import RawArticle
from .serializers import ArticleListSerializer, ArticleDetailSerializer
from rest_framework.permissions import IsAuthenticated


class ArticleListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        return RawArticle.objects.all().order_by("-published_at", "-scraped_at")


class ArticleDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = RawArticle.objects.all()
    serializer_class = ArticleDetailSerializer