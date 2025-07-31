from rest_framework import permissions

# Custom permission for role ADMIN
class IsUserAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'ADMIN'
    
# Custom permission to be editable for role ADMIN and readable for roles DOCTOR and STAFF
class IsReadOnlyForRoles(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # For safe methods (like GET), allow access if the role is appropriate.
        if request.method in permissions.SAFE_METHODS:
            return request.user.role in ['ADMIN', 'DOCTOR', 'STAFF']

        # For unsafe methods (like PUT, PATCH, DELETE), only allow admins.
        return request.user.role == 'ADMIN'

# Custom permission to be editable for all roles except role USER
class IsEditableForRoles(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role in ['ADMIN', 'DOCTOR', 'STAFF']