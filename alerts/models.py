from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from account.models import Team

class Alert(models.Model):
    
    #these are choices for status of alert
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        ASSIGNED = 'ASSIGNED', _('Assigned')
        IN_PROCESS = 'IN_PROCESS', _('In Process')
        PROCESS_ENDING = 'PROCESS_ENDING', _('Process Ending')
        CLOSED = 'CLOSED', _('Closed')

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=255, help_text="e.g., Ward 4, Room 201B")
    
    # This field will be set automatically
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        editable=False, 
        related_name='created_alerts'
    )
    assigned_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_alerts'
    )
    
    # Descriptions
    doctor_description = models.TextField(null=True, blank=True, help_text="Description for doctors.")
    staff_description = models.TextField(null=True, blank=True, help_text="Description for general staff.")
    admin_description = models.TextField(null=True, blank=True, help_text="Internal description for administrators.")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True # Add index for faster filtering on status
    )
   
    image = models.ImageField(
        upload_to='alert_images/', 
        null=True, 
        blank=True, 
        help_text="Optional image related to the alert."
    )

    # Timestamps
    
    #When alert created on device, get from client side
    created_time = models.DateTimeField(blank=True)
    
    #when alert recieved by the server
    recieved_time = models.DateTimeField(auto_now_add=True)    

    assigned_date = models.DateTimeField(null=True, blank=True)
    in_process_date = models.DateTimeField(null=True, blank=True)
    process_ending_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    class Meta:
        ordering = ['-created_time'] # Show the newest alerts first