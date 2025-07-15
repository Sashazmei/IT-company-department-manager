from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
