"""Ride ratings models"""

#django
from django.db import models

#utilities
from cride.utils.models import CRideModel


class Rating(CRideModel):
    """Rating that user gave to the ride"""

    ride = models.ForeignKey('rides.Ride', on_delete=models.CASCADE, related_name='rated_ride')
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
    rating_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, help_text='User that emits the rating', related_name='rating_user')
    rated_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, help_text='User is being rated', related_name='rated_user')

    comments= models.TextField(blank=True)

    rating = models.IntegerField(default=1)

    def __str__(self):
        """Return the summary"""
        return '@{} rated {} @{}'.format(
            self.rating_user.username,
            self.rating,
            self.rated_user.username,
        )
