from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include URLs from 'account' app
    path('api/', include('account.urls')),
    # Include URLs from 'services' app
    path('api/', include('services.urls')),
    # Include URLs from 'Alerts' app
    path('api/', include('alerts.urls')),
]