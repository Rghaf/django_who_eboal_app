from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Team

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Add 'role' to the list display
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']

    # Add 'role' to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_img')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'profile_img')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('services', 'members')
