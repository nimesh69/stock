from django.urls import path
from .views import CompanyListView, CompanyPriceListView

urlpatterns = [
    path("companies", CompanyListView.as_view(), name="company-list"),
    path("companies/<int:pk>/prices", CompanyPriceListView.as_view(), name="company-prices"),
]