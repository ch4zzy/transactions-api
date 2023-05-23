from django.urls import include, path
from rest_framework import routers

from apps.customer.views import ProfileBalanceView

app_name = "api_customer"

router = routers.DefaultRouter()
router.register(r"profiles", ProfileBalanceView)

urlpatterns = [
    path("", include(router.urls)),
]
