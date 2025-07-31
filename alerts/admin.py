from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """
    Admin view for the Alert model, configured to handle related fields.
    """
    list_display = ('name', 'status', 'location', 'creator_user', 'assigned_team', 'created_time')
    list_filter = ('status', 'created_time', 'assigned_team')
    search_fields = ('name', 'location', 'creator_user__username', 'assigned_team__name')
    
    # Use raw_id_fields for ForeignKey fields with many options for better performance.
    # This changes the dropdown for 'assigned_team' to a more efficient lookup widget.
    raw_id_fields = ('assigned_team',)
    
    # Make timestamp and creator fields read-only as they are set by the system.
    readonly_fields = ('recieved_time', 'creator_user')

    # Organize the edit form into sections for better readability.
    fieldsets = (
        ('Core Information', {
            'fields': ('name', 'location', 'status', 'assigned_team', 'creator_user', 'image')
        }),
        ('Role-Based Descriptions', {
            'classes': ('collapse',), # Make this section collapsible
            'fields': ('doctor_description', 'staff_description', 'admin_description'),
        }),
        ('Lifecycle Timestamps', {
            'fields': ('created_time', 'recieved_time', 'assigned_date', 'in_process_date', 'process_ending_date', 'closed_date'),
        }),
    )

    def save_model(self, request, obj, form, change):
        #Save the creator user automatically
        if not obj.pk: # If the object is new (has no primary key yet)
            obj.creator_user = request.user
        super().save_model(request, obj, form, change)