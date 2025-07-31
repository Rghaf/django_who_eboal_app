from rest_framework import serializers
from .models import Alert
from account.serializers import UserSerializer
from django.utils import timezone 

class AlertSerializer(serializers.ModelSerializer):
    
    #creator user will add automatically
    creator_user = UserSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id', 'name', 'location', 'creator_user', 'assigned_team',
            'doctor_description', 'staff_description', 'admin_description',
            'status', 'image', 'created_time', 'recieved_time', 'assigned_date',
            'in_process_date', 'process_ending_date', 'closed_date'
        ]
        # These fields are set automatically by the system or are not required when a client creates an alert.
        read_only_fields = [
            'id', 'creator_user', 'recieved_time', 'assigned_date',
            'in_process_date', 'process_ending_date', 'closed_date'
        ]

    def create(self, validated_data):

        # The request object is passed to the serializer's context by the view.
        user = self.context['request'].user
        validated_data['creator_user'] = user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Override the update method to automatically set timestamps when the
        status of an alert changes.
        """
        # Check if 'status' is being updated and if it's a new value.
        if 'status' in validated_data and validated_data['status'] != instance.status:
            new_status = validated_data['status']
            
            # Set the correct timestamp based on the new status.
            if new_status == Alert.Status.IN_PROCESS and not instance.in_process_date:
                instance.in_process_date = timezone.now()
            elif new_status == Alert.Status.PROCESS_ENDING and not instance.process_ending_date:
                instance.process_ending_date = timezone.now()
            elif new_status == Alert.Status.CLOSED and not instance.closed_date:
                instance.closed_date = timezone.now()
        
        # Manually update all fields from validated_data onto the instance.
        # This ensures all changes are applied before the final save.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Save all changes (both timestamps and validated data) to the database.
        instance.save()
        
        return instance

class AlertCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        # Only include fields required or optional at creation.
        fields = [
            'name', 'location', 'doctor_description', 
            'staff_description', 'admin_description', 'created_time'
        ]
        # Make description fields optional, as only one will be used per role.
        extra_kwargs = {
            'doctor_description': {'required': False},
            'staff_description': {'required': False},
            'admin_description': {'required': False},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creator_user'] = user
        return super().create(validated_data)

    def validate(self, data):
        user_role = self.context['request'].user.role

        # Users can just write description for the specific field which is match with their role
        if user_role != 'ADMIN' and 'admin_description' in data and data['admin_description']:
            raise serializers.ValidationError("Only Admins can provide an admin description.")
        
        if user_role != 'DOCTOR' and 'doctor_description' in data and data['doctor_description']:
            raise serializers.ValidationError("Only Doctors can provide a doctor description.")
            
        if user_role != 'STAFF' and 'staff_description' in data and data['staff_description']:
            raise serializers.ValidationError("Only Staff can provide a staff description.")

        return data
    
class AlertTeamAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['assigned_team']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        if validated_data.get('assigned_team'):
            instance.status = Alert.Status.ASSIGNED
            instance.assigned_date = timezone.now()
            instance.save()

        return instance