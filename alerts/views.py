from rest_framework import generics, permissions
from .models import Alert
from .serializers import AlertSerializer, AlertTeamAssignedSerializer
from account.permissions import IsEditableForRoles, IsUserAdmin

# Reusable Mixin for Role-Based Filtering 
class FilteredAlertListMixin:
    def get_queryset(self):
        user = self.request.user
        # Get the initial queryset from the view 
        queryset = super().get_queryset()

        if user.role == 'ADMIN':
            # Admins see everything
            return queryset 

        if user.role in ['DOCTOR', 'STAFF']:
            # Filter for alerts where the user is a member of the assigned team
            return queryset.filter(assigned_team__members=user)

        # Other roles (like a base 'USER') see nothing by default
        return queryset.none()


 # API for get list of all alerts or create a new one
class AlertListCreateAPIView(FilteredAlertListMixin, generics.ListCreateAPIView):
    queryset = Alert.objects.all().order_by('-recieved_time')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated, IsEditableForRoles]

    def get_serializer_context(self):
        return {'request': self.request}

# Get, update or delete a specific alert
class AlertDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated, IsEditableForRoles]

# API to assigne a team to an alert, just can be done by an ADMIN
class AlertTeamAssignedAPIView(generics.UpdateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertTeamAssignedSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAdmin]

# Get list of alerts with pending status
class AlertPendingListAPIView(FilteredAlertListMixin, generics.ListAPIView):
    queryset = Alert.objects.filter(status=Alert.Status.PENDING).order_by('-recieved_time')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

# Get list of alerts with assigned status
class AlertAssignedListAPIView(FilteredAlertListMixin, generics.ListAPIView):
    queryset = Alert.objects.filter(status=Alert.Status.ASSIGNED).order_by('-recieved_time')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

# Get list of alerts with in process status
class AlertInProcessListAPIView(FilteredAlertListMixin, generics.ListAPIView):
    queryset = Alert.objects.filter(status=Alert.Status.IN_PROCESS).order_by('-recieved_time')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

# get list of alerts with process ending status
class AlertProcessEndingListAPIView(FilteredAlertListMixin, generics.ListAPIView):
    queryset = Alert.objects.filter(status=Alert.Status.PROCESS_ENDING).order_by('-recieved_time')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

# get list of all closed alerts
class AlertClosedListAPIView(FilteredAlertListMixin, generics.ListAPIView):
    queryset = Alert.objects.filter(status=Alert.Status.CLOSED).order_by('-recieved_time')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]