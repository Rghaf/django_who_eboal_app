from django.urls import path
from .views import (
    AlertListCreateAPIView, 
    AlertDetailAPIView,
    AlertTeamAssignedAPIView,
    AlertPendingListAPIView,
    AlertAssignedListAPIView,
    AlertInProcessListAPIView,
    AlertProcessEndingListAPIView,
    AlertClosedListAPIView
)

urlpatterns = [
    # listing all alerts (GET, filtered by role) and creating a new one (POST)
    path('alerts/', AlertListCreateAPIView.as_view(), name='alert-list-create'),
    
    # retrieving (GET), updating (PUT/PATCH), and deleting (DELETE) a specific alert
    path('alerts/<int:pk>/', AlertDetailAPIView.as_view(), name='alert-detail'),
    
    # updating just the assigned team of an alert (PATCH)
    path('alerts/<int:pk>/assign-team/', AlertTeamAssignedAPIView.as_view(), name='alert-assign-team'),
    
    # Each of these handles a GET request to list alerts of a specific status, filtered by user role.
    path('alerts/pending/', AlertPendingListAPIView.as_view(), name='alert-list-pending'),
    path('alerts/assigned/', AlertAssignedListAPIView.as_view(), name='alert-list-assigned'),
    path('alerts/in-process/', AlertInProcessListAPIView.as_view(), name='alert-list-in-process'),
    path('alerts/process-ending/', AlertProcessEndingListAPIView.as_view(), name='alert-list-process-ending'),
    path('alerts/closed/', AlertClosedListAPIView.as_view(), name='alert-list-closed'),
]