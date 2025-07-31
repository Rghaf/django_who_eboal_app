from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, RegisterSerializer, TeamSerializer, UserRoleUpdateSerializer
from .models import CustomUser, Team
from .permissions import IsUserAdmin, IsReadOnlyForRoles

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny] # Allow any user to register

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token.",
        })

# Login API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
# List of all users (without considering role) 
class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAdmin]

# List of all users with role DOCTOR
class RoleDoctorListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='DOCTOR').order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAdmin]

# List of all users with role STAFF
class RoleStaffListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='STAFF').order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAdmin]

# List of all users with role USER
class RoleUserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='USER').order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAdmin]

# Update user role, remove user or retrive user details
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsReadOnlyForRoles]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserRoleUpdateSerializer
        return UserSerializer
    
# Create Team API
class TeamCreateAPIView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAdmin]

# Get list of all teams (only accessable for role ADMIN)
class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAdmin]
    
# Get, Update and remove API for a team
class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadOnlyForRoles]
