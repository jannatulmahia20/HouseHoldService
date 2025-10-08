from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path("", home, name="home"),  
    path("admin/", admin.site.urls),
    path("register/", include("core.urls")),  
    # path("api/", include("core.api_urls")),  
]
