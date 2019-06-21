"""Cride Memberships Models"""

#django
from django.db import models

#Utilities
from cride.utils.models import CRideModel


class Membership(CRideModel):
    """A membership model
    table that holds the membership between a user and a circle"""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    is_admin = models.BooleanField('circle admin', default=False, help_text="circle admin can update data and manage it's membership")

    #invitation
    used_invitation = models.PositiveSmallIntegerField(default=0)
    remaining_invitation = models.PositiveSmallIntegerField(default=0)
    invited_by = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL, related_name='invited_by')   

    #stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)

    #status
    is_active = models.BooleanField('active status', default=True, help_text='Only active users are allowed to interact with the circle')
    
    def __str__(self):
        """Returns a username and circle"""
        return '@{} at #{}'.format(self.user.username, self.circle.slug_name)

