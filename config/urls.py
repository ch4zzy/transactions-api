from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
