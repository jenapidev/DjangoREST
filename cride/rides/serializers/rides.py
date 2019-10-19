"""Rides Serializer"""

#Django rest Framework
from rest_framework import serializers

#Models
from cride.rides.models import Ride
from cride.circles.models import Membership
from cride.users.models import User

#Utilities
from datetime import timedelta
from django.utils import timezone

#Serializers
from cride.users.serializers import UserModelSerializer


class RideModelSerializer(serializers.ModelSerializer):
    """Ride Model Serializer"""

    offered_by = UserModelSerializer(read_only=True)
    offered_in = serializers.StringRelatedField()

    passengers = UserModelSerializer(read_only=True, many=True)

    class Meta:
        """Meta class"""
        model = Ride
        fields = '__all__'
        read_only_fields = (
            'offered_by',
            'offered_in',
            'rating'
        )



class CreateRideSerializer(serializers.ModelSerializer):
    """Create ride serializer"""

    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    availiable_seats = serializers.IntegerField(min_value=1, max_value=15)


    class Meta:
        """Meta class"""

        model = Ride
        exclude = ('offered_in', 'passengers', 'rating', 'is_active')

    def validate_departure_date(self, data):
        """Verify date is not in the past"""
        min_date = timezone.now() + timedelta(minutes=10)
        if data <= min_date:
            raise serializers.ValidationError('Departure rides must be at least pass the next 20 minutes window.')
        return data

    def validate(self, data):
        """Validate.
        Verify that the person who offers the ride is member
        and also the same user making the request.
        """
        if self.context['request'].user != data['offered_by']:
            raise serializers.ValidationError('Rides offered on behalf of others are not allowed.')

        user = data['offered_by']
        circle = self.context['circle']
        try:
            membership = Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')

        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError('Departure date must happen after arrival date.')

        self.context['membership'] = membership
        return data


    def create(self, data):
        """Create ride and upgdate stats"""
        circle = self.context['circle']
        ride = Ride.objects.create(**data, offered_in=circle)
        membership = self.context['membership']

        #circle
        circle.rides_offered += 1
        circle.save()

        #membership
        membership.rides_offered += 1
        membership.save()

        #profile
        profile = data['offered_by'].profile
        profile.rides_offered += 1

        profile.save()
        return ride

    def update(self, instance, data):
        """Update ride if the ride is before departure date"""
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializers.ValidationError('On going ride ca not be updated')
        return super(RideModelSerializer, self).update(instance, data)


class JoinRideSerializer(serializers.ModelSerializer):
    """Join ride serializer"""

    passenger = serializers.IntegerField()

    class Meta:
        """Meta class"""
        model = Ride
        fields = ('passenger',)

    def validate_passenger(self, data):
        """Verify if user exists and is not in the ride"""
        try:
            user = User.objects.get(pk=data)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid passenger.')

        circle = self.context['circle']
        try:
            membership = Membership.objects.get(user=user, circle=circle, is_active=True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')

        self.context['user'] = user
        self.context['member'] = membership
        return data

    def validate(self, data):
        """verify if rides allow new passengers"""
        offset = timezone.now()
        ride = self.context['ride']

        #Date Validation
        if ride.departure_date <= offset:
            raise serializers.ValidationError("You can't join this ride, because it's has departed")

        #Ride availiable seats Validation
        if ride.availiable_seats < 1:
            raise serializers.ValidationError('Ride has not availiable seats')

        #Passengers joining only one time per ride


        if ride.passengers.filter(pk=self.context['user'].pk).exists():
            raise serializers.ValidationError('Passenger has already joined into this ride')

        return data

    def update(self, instance, data):
        """Update stats when passenger join to the ride"""
        ride = self.context['ride']
        circle = self.context['circle']
        user = self.context['user']

        ride.passengers.add(user)
        ride.availiable_seats -= 1
        ride.save()

        #Profile update
        profile = user.profile
        profile.rides_taken += 1
        profile.save()

        #Membership update
        member = self.context['member']
        member.rides_taken += 1
        member.save()

        #circle update
        circle.rides_taken += 1
        circle.save()

        return ride

class EndRideSerializer(serializers.ModelSerializer):
    """End Ride Serializer"""

    current_time = serializers.DateTimeField()

    class Meta:
        """Meta class"""

        model = Ride
        
