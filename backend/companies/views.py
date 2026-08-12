import re
from datetime import timedelta, datetime

from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Company, DailyPrice
from .serializers import CompanyListSerializer, DailyPriceSerializer
from rest_framework.permissions import IsAuthenticated

RANGE_RE = re.compile(r"^(\d+)([dy])$")
DEFAULT_RANGE_DAYS = 30


class CompanyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all().order_by("symbol")
    serializer_class = CompanyListSerializer


class CompanyPriceListView(generics.ListAPIView):
    """
    /api/companies/5/prices	last 30 days (default)
    /api/companies/5/prices?range=90d	last 90 days
    /api/companies/5/prices?range=1y	last 1 year
    /api/companies/5/prices?range=all	full history
    /api/companies/5/prices?from=2026-01-01&to=2026-03-31	explicit date range
    /api/companies/5/prices?from=2026-06-01	from that date to today
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DailyPriceSerializer

    def get_queryset(self):
        company_id = self.kwargs["pk"]
        qs = DailyPrice.objects.filter(company_id=company_id)

        params = self.request.query_params
        date_from = params.get("from")
        date_to = params.get("to")
        range_param = params.get("range")

        if date_from or date_to:
            # explicit date-wise filtering takes priority over `range`
            if date_from:
                qs = qs.filter(date__gte=self._parse_date(date_from, "from"))
            if date_to:
                qs = qs.filter(date__lte=self._parse_date(date_to, "to"))
        elif range_param == "all":
            pass  # no filtering
        else:
            # use given range, or default to 30 days
            days = self._parse_range(range_param) if range_param else DEFAULT_RANGE_DAYS
            cutoff = timezone.now().date() - timedelta(days=days)
            qs = qs.filter(date__gte=cutoff)

        return qs.order_by("date")

    @staticmethod
    def _parse_range(range_param):
        match = RANGE_RE.match(range_param)
        if not match:
            raise ValidationError(
                {"range": "Invalid format. Use e.g. '7d', '30d', '90d', '1y', or 'all'."}
            )
        value, unit = match.groups()
        value = int(value)
        return value * 365 if unit == "y" else value

    @staticmethod
    def _parse_date(value, field_name):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError(
                {field_name: "Invalid date format. Use YYYY-MM-DD."}
            )