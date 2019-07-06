"""Circles Permissions"""

#Rest framework
from rest_framework.permissions import BasePermission

#Models
from cride.circles.models import Membership

class IsActiveCircleMember(BasePermission):
    """Allow access to only circle's members"""

    def has_permission(self, request, view):
        """Verify if user's part of the circle and if is an active member"""

        try:
            Membership.objects.get(user=request.user, circle=view.circle, is_active=True)
        except Membership.DoesNotExist:
            return False
        return True

class IsSelfMember(BasePermission):

    def has_permission(self, request, view):

        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):

        return request.user == obj.user