from django.urls import path
from .views import CompanyListView, CompanyPriceListView
from analysis.views import BehaviorSummaryListView

urlpatterns = [
    path("", CompanyListView.as_view(), name="company-list"),
    path("<int:pk>/prices", CompanyPriceListView.as_view(), name="company-prices"),
    path("<int:pk>/behavior-summary", BehaviorSummaryListView.as_view(), name="company-behavior-summary"),
]