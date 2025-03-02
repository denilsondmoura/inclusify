from pathlib import Path, os
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(str(os.getenv('ADMIN_URL')), admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
