"""Circles model"""

#django 
from django.db import models

#utilities
from cride.utils.models import CRideModel


class Circles(CRideModel):
    """circle model
    A circle is a private group where rides are taken and offered 
    To Join a circle you must have a unique invitation provided by an existing member
    """

    name = models.CharField('circle name', max_length=140)
    slug_name = models.CharField(unique=True , max_length=50)

    about = models.CharField('circle descirption', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)

    #Stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField('verified circle', default=False, help_text='verified circles are also known as official communities')
    is_public = models.BooleanField(default=True, help_text='Publick circles are listed in main page, everyone knows about their existance.')

    is_limited = models.BooleanField('limited', default=False, help_text='Limited circles can grow up to a limited number of members.')
    numbers_limit = models.IntegerField(default=0, help_text='if circle is limited, this will be the number of users con be added')

    def __str__(self):
        """return circle name"""
        return self.name

    class Meta(CRideModel.Meta):
        """Meta class"""
        ordering = ['-rides_taken', '-rides_offered']