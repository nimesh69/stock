from django.urls import path
from .views import ArticleListView, ArticleDetailView,CompanyArticleListView

urlpatterns = [
    path("", ArticleListView.as_view(), name="article-list"),
    path("<int:pk>", ArticleDetailView.as_view(), name="article-detail"),
    path("<int:pk>/news", CompanyArticleListView.as_view(), name="company-article-list"),
]