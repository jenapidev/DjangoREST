"""Circle Permissioins Classes"""

#Django Rest Framework
from rest_framework.permissions import BasePermission

#Models
from cride.circles.models import Membership


class IsCircleAdmin(BasePermission):
    """Allow permissions only for admins to change or update a circle"""

    def has_object_permission(self, request, view, obj):
        """Check if user have a membership in the obj"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True