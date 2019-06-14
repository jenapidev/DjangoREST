"""Circle serializers"""

#django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#models
from cride.circles.models import Circle

class CircleSerializer(serializers.Serializer):
    """Circle serializer"""

    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    numbers_limit = serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):
    """create circle serializer"""

    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(max_length=40, validators=[
        UniqueValidator(queryset=Circle.objects.all())
    ])
    about = serializers.CharField(max_length=255, required=False)

    def create(self, data):
        """Create circle"""
        circle = Circle.objects.create(**data)