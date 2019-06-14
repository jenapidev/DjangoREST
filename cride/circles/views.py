"""Circles Views"""

#django_rest_framework
from rest_framework.decorators import api_view 
from rest_framework.response import Response

#models
from cride.circles.models import Circle

#serializer
from cride.circles.serializers import CircleSerializer, CreateCircleSerializer


@api_view(['GET'])
def list_circles(request):
    """list circles"""
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_circle(request):
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    Circle = serializer.save()
    return Response(CircleSerializer(circle).data)

