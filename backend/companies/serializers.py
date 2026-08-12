from rest_framework import serializers
from .models import Company, DailyPrice


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "symbol", "name", "sector"]


class DailyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPrice
        fields = ["date", "open", "high", "low", "close", "volume", "turnover"]