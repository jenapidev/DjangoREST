"""Profile serializer"""

#Django rest framework
from rest_framework import serializers

#Models 
from cride.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile Model serializer"""

    class Meta:
        """Meta Class"""

        model = Profile
        fields = (
            'picture',
            'biography',
            'rides_taken',
            'rides_offered',
            'reputation'
        )

        read_only_fields = (
            'rides_taken',
            'rides_offered',
            'reputation'
        )