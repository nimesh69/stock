from django.urls import path
from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path("news", ArticleListView.as_view(), name="article-list"),
    path("news/<int:pk>", ArticleDetailView.as_view(), name="article-detail"),
]