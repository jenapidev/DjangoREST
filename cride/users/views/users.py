"""Users View"""

#django REST framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

#serializers
from cride.users.serializers import (UserLoginSerializer, UserSignupSerializer, UserModelSerializer)


class UserLoginAPIView(APIView):
    """User login API view"""

    def post(self, request, *args, **kwargs):
        """Handle HTTP request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserSignupAPIView(APIView):
    """User Sign up view"""

    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)