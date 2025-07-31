from django.urls import path
from .views import ServiceListCreateAPIView, ServiceDetailAPIView

urlpatterns = [
    # Retrive list of all services and create a new service
    path('services/', ServiceListCreateAPIView.as_view(), name='service-list-create'),
    
    # Get a specific service, remove and update it (accessable just for ADMIN role)
    path('services/<int:pk>/', ServiceDetailAPIView.as_view(), name='service-detail'),

]