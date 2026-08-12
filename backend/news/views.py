from rest_framework import generics
from .models import RawArticle, Company
from rest_framework.exceptions import NotFound
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

class CompanyArticleListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        company_id = self.kwargs["pk"]
        if not Company.objects.filter(pk=company_id).exists():
            raise NotFound("Company not found.")

        return (
            RawArticle.objects.filter(categories__company_id=company_id)
            .order_by("-published_at", "-scraped_at")
            .distinct()
        )