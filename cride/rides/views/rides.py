"""Rides Views"""

#Django rest framework
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response


#Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.rides.permissions.rides import IsRideOwner, IsNotRideOwner


#Serializers
from cride.rides.serializers import (
    CreateRideSerializer,
    RideModelSerializer,
    JoinRideSerializer,
    EndRideSerializer,
    CreateRideRatingSerializer,
    )

#Filters
from rest_framework.filters import SearchFilter, OrderingFilter

#Models
from cride.circles.models import Circle

#Utilities
from datetime import timedelta
from django.utils import timezone


class RideViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated, IsActiveCircleMember]
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('departure_date', 'arrival_location', 'arrival_date', 'availiable_seats')
    ordering_fields = ('departure_date', 'arrival_date', 'arrival_location', 'availiable_seats')
    search_fields = ('departure_location', 'departure_date', 'arrival_location')

    def dispatch(self, request, *args, **kwargs):
        """Verify if circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on actions"""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update', 'partial_update', 'finish']:
            permissions.append(IsRideOwner)
        if self.action == 'join':
            permissions.append(IsNotRideOwner)
        if self.action == 'finish':
            return EndRideSerializer
        return [p() for p in permissions]


    def get_serializer_context(self):
        """Add circle to te serializer context"""
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context

    def get_serializer_class(self):
        """Retrun serializer based on actions"""
        if self.action == 'create':
            return CreateRideSerializer
        if self.action in ['update', 'partial_update']:
            return JoinRideSerializer
        if self.action == 'join':
            return JoinRideSerializer
        if self.action == 'finish':
            return EndRideSerializer
        if self.action == 'rate':
            return CreateRideRatingSerializer
        return RideModelSerializer

    def get_queryset(self):
        """Return active circles rides"""
        offset = timezone.now() + timedelta(minutes=10)
        return self.circle.ride_set.filter(
            departure_date__gte=offset,
            is_active=True,
            availiable_seats__gte=1
        )

    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        """Add user to ride"""
        ride = self.get_object()
        serialixer_class = self.get_serializer_class()
        serializer = serialixer_class(
            ride,
            data={'passenger': request.user.pk},
            context={'ride': ride, 'circle': self.circle},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        """Finish a ride"""
        ride = self.get_object()
        serializer_class = self.serializer_class()
        serializer = serializer_class(
            ride,
            data={'is_active': False, 'current_time': timezone.now()},
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def rate(self, request, *args, **kwargs):
        """Rate ride."""
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        context['ride'] = ride
        serializer = serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_201_CREATED)
