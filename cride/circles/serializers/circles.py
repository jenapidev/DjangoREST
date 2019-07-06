"""Circles Serializers"""

#rest framework
from rest_framework import serializers

#Model
from cride.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer"""

    numbers_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=32000
    )
    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """Meta Class"""
        model = Circle
        fields = (
            'name', 'slug_name',
            'about', 'picture',
            'rides_offered', 'rides_taken',
            'verified', 'members', 'is_public',
            'is_limited', 'numbers_limit'
        )
        read_only_fields = (
            'is_public',
            'verified',
            'rides_offered',
            'rides_taken'
        )
    
    def validate(self, data):
        """Ensure both numbers_limit and is_limited are present"""

        numbers_limit = data.get('numbers_limit', None)
        is_limited = data.get('is_limited', False)
        if is_limited ^ bool(numbers_limit):
            raise serializers.ValidationError('You must have a members limit if want to make your circle limited.')
        return data