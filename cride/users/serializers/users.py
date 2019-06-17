"""Users Serializer"""

#django
from django.contrib.auth import authenticate

#django res framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

#models
from cride.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )

class UserSignupSerializer(serializers.Serializer):
    """User sign up serializer.
    Handle sign up data validations and user/profile creation"""
    

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
        self.context['user'] = user
        return data


    def create(self, data):
        """generates or retrieve a new token"""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
