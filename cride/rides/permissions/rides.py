"""Rides permissions"""

#Django rest framework
from rest_framework.permissions import BasePermission


class IsRideOwner(BasePermission):
    """Verify if requesting users has owner account permissions"""

    def has_object_permission(self, request, view, obj):
        """Verify if requesting users is the creator of the object to modify"""
        return request.user == obj.offered_by

class IsNotRideOwner(BasePermission):
    """Verify if requesting user is owner"""

    def has_object_permission(self, request, view, obj):
        """Verify if requesting users is the creator of the object"""
        return not request.user == obj.offered_by
