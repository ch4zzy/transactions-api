from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.customer.urls", namespace="api_profile")),
    path("api/", include("apps.transactions.urls", namespace="api_transactions")),
]

urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
