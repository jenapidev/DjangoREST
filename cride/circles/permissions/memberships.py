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

class IsAdminOrMembershipOwner(BasePermission):
    """Allow Only admins or membership owners do execute an action"""

    def has_permission(self, request, view):
        """Verify if user's part of the circle and if is an active member"""

        membership = view.get_object()
        if membership.user == request.user:
            return True

        try:
            Membership.objects.get(user=request.user, circle=view.circle, is_active=True, is_admin=True)
        except Membership.DoesNotExist:
            return False
        return True
