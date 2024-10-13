from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'profile_image']

    def create(self, validated_data): 
        username = validated_data['username']
        first_name = validated_data.get('first_name', 'Not Set') 
        last_name = validated_data.get('last_name', 'Not Set')   
        email = validated_data['email']
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        profile_image = validated_data.get('profile_image', None) 

        if password != confirm_password:
            raise serializers.ValidationError({"error": "Passwords didn't match!"})

        user = CustomUser(username=username, first_name=first_name, last_name=last_name, email=email, profile_image=profile_image)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        return instance

    
class UserLoginSerializer(serializers.Serializer):
    username= serializers.CharField(required= True)
    password= serializers.CharField(required= True)

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        # Check if the old password is correct
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is not correct."})

        # Check if the new passwords match
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"confirm_new_password": "New passwords do not match."})

        return attrs

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']

        # Set the new password
        user.set_password(new_password)
        user.save()

        return user
