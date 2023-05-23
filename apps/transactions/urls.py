from django.urls import include, path
from rest_framework import routers

from apps.transactions.views import (
    TransactionAPIView,
    TransactionsViewSet,
    WithdrawalsAPIView,
)

app_name = "api_transactions"

router = routers.DefaultRouter()

router.register(r"operation", TransactionsViewSet, basename="operation")


urlpatterns = [
    path("transaction/", TransactionAPIView.as_view(), name="transaction"),
    path("withdrawal/", WithdrawalsAPIView.as_view(), name="withdrawal"),
    path("", include(router.urls)),
]
