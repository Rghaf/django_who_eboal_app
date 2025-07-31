from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from services.models import Service

#we use abstract user for adding new fields to django user model
#this is our new user model
class CustomUser(AbstractUser):
    #User Roles
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        DOCTOR = 'DOCTOR', 'Doctor'
        STAFF= 'STAFF', 'Staff'
        USER = 'USER', 'User'
        
    profile_img = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_groups",  # Unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions", # Unique related_name
        related_query_name="user",
    )
    
    def __str__(self):
        return self.username
    


#Each team includes members and can provide one or more services
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Many-to-many relationship with Service
    services = models.ManyToManyField(Service, related_name='services', blank=True)
    
    # Many-to-many relationship with the CustomUser model
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='teams', # Helps in querying from the user side (e.g., user.teams.all())
        blank=True
    )

    def __str__(self):
        return self.name
    
    
    

