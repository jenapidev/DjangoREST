"""Membership serializers"""

#Django rest framework
from rest_framework import serializers

#Models
from cride.circles.models import Membership

#Serializers
from cride.users.serializers import UserModelSerializer

class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer"""

    user = UserModelSerializer(read_only=True)
    joined_at = serializers.DateTimeField(source='created', read_only=True)


    class Meta:
        """Meta class"""
        model = Membership
        fields = (
            'user',
            'is_admin', 'is_active',
            'used_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
            'joined_at',
        )

        read_only = (
            'user', 
            'used_invitations',
            'invited_by',
            'rides_taken',
            'rides_offered',
        )