from rest_framework import generics, permissions
from .models import Service
from .serializers import ServiceSerializer
from account.permissions import IsReadOnlyForRoles, IsUserAdmin

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadOnlyForRoles]
    
class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAdmin]