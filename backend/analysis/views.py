from datetime import timedelta, datetime
from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import ValidationError, NotFound

from companies.models import Company
from .models import BehaviorSummary
from .serializers import BehaviorSummarySerializer
from companies.views import CompanyPriceListView  # reuse _parse_range / _parse_date

DEFAULT_RANGE_DAYS = 30


class BehaviorSummaryListView(generics.ListAPIView):
    serializer_class = BehaviorSummarySerializer

    def get_queryset(self):
        company_id = self.kwargs["pk"]
        if not Company.objects.filter(pk=company_id).exists():
            raise NotFound("Company not found.")

        qs = BehaviorSummary.objects.filter(company_id=company_id)
        params = self.request.query_params
        date_from, date_to, range_param = params.get("from"), params.get("to"), params.get("range")

        if date_from or date_to:
            if date_from:
                qs = qs.filter(date__gte=CompanyPriceListView._parse_date(date_from, "from"))
            if date_to:
                qs = qs.filter(date__lte=CompanyPriceListView._parse_date(date_to, "to"))
        elif range_param == "all":
            pass
        else:
            days = CompanyPriceListView._parse_range(range_param) if range_param else DEFAULT_RANGE_DAYS
            cutoff = timezone.now().date() - timedelta(days=days)
            qs = qs.filter(date__gte=cutoff)

        return qs.order_by("date")