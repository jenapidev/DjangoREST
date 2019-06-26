"""Users View"""

#django REST framework
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

#serializers
from cride.users.serializers import (UserLoginSerializer, UserSignupSerializer, UserModelSerializer, AccountVerificationSerializer)


class UserViewSet(viewsets.GenericViewSet):
    """User view set.
    Signup, login and accoutn verifications"""

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User signup"""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification"""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations... Now you can use your Comparte Ride account'}
        return Response(data, status=status.HTTP_200_OK)

        