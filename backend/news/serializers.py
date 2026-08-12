from rest_framework import serializers
from .models import RawArticle


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawArticle
        fields = ["id", "headline", "source_portal", "published_at"]


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawArticle
        fields = ["id", "headline", "body", "url", "source_portal", "published_at"]