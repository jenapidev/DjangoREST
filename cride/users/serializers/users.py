"""Users Serializer"""

#django
from django.contrib.auth import authenticate

#django res framework
from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    """User Login Serializer
    handle the login request data"""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        """Check credentials"""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        return data
