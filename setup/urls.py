from pathlib import Path, os
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(str(os.getenv('ADMIN_URL')), admin.site.urls),
    path('home', include('apps.core.urls')),
]
