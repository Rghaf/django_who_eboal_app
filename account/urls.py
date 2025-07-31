from django.urls import path
from .views import RegisterAPI, UserAPI, TeamCreateAPIView, TeamDetailAPIView, TeamListAPIView, UserListAPIView, RoleDoctorListAPIView, RoleStaffListAPIView, RoleUserListAPIView, UserDetailAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Endpoint for user registration
    path('register/', RegisterAPI.as_view(), name='register'),
    
    # Endpoint for user login (obtaining a token pair)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Endpoint for refreshing an access token
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Endpoint to get current user's data
    path('user/', UserAPI.as_view(), name='user_api'),
    
    # Endpoint to get list of users
    path('users/', UserListAPIView.as_view(), name='user-list-all'),
    path('users/doctors/', RoleDoctorListAPIView.as_view(), name='user-list-doctors'),
    path('users/staff/', RoleStaffListAPIView.as_view(), name='user-list-staff'),  
    path('users/regular/', RoleUserListAPIView.as_view(), name='user-list-regular'),
    
    # Get, romove or update a specific user
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'), # Handles GET, PATCH, DELETE for a specific user

    # Endpoint for create team
    path('teams/create/', TeamCreateAPIView.as_view(), name='team-create'),
    
    # Endpoint for retrive list of teams
    path('teams/', TeamListAPIView.as_view(), name='team-list'), # NEW URL

    # Endpoint for updating, remove or get a team (DOCTOR and STAFF can only use GET method)
    path('teams/<int:pk>/edit/', TeamDetailAPIView.as_view(), name='team-edit'),
]