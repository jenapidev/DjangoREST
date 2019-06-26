"""Cride Users Permisions"""

#django rest framework
from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    """Allow acces to objects only to owners"""

    def has_object_permission(self, request, view, obj):
        """Check object and user"""
        return request.user == obj
        