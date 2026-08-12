from rest_framework import serializers
from .models import BehaviorSummary


class BehaviorSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorSummary
        fields = ["date", "vwap", "close", "pressure_indicator", "is_volume_anomaly", "avg_volume_20d"]