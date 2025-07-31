from rest_framework import serializers
from .models import CustomUser, Team, Service

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Fields to include in the serialized output
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
        
# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password', style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        # Fields required for registration
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove the password fields from the validated data, as we'll handle them manually.
        password = validated_data.pop('password')
        validated_data.pop('password2')

        # Create the user instance with the remaining validated data.
        user = CustomUser(**validated_data)

        # Use set_password() to hash the password correctly.
        user.set_password(password)
        
        # Save the user to the database.
        user.save()
        
        return user
    
class TeamSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), 
        many=True,
        required=True # A team must have services
    )
    members = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), 
        many=True, 
        required=False # Members can be added later
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'services', 'members']

    def validate_services(self, value):
        if not (1 <= len(value) <= 4):
            raise serializers.ValidationError("A team must have between 1 and 4 services.")
        return value
    
class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['role']