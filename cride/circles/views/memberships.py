"""Circles memberships views"""

#Django Rest Framework
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404


#Serializers
from cride.circles.serializers.memberships import MembershipModelSerializer
from cride.users.serializers.users import UserModelSerializer


#Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.circles.permissions.memberships import IsAdminOrMembershipOwner


#Models
from cride.circles.models import Circle, Membership


class MembershipViewSet(mixins.ListModelMixin,  mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Circle Membership View Set"""


    user = UserModelSerializer(read_only=True)
    serializer_class = MembershipModelSerializer
    

    def dispatch(self, request, *args, **kwargs):
        """Verify if circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    
    def get_permissions(self):
        """Asign permissions based on actions"""
        permissions = [IsAuthenticated, IsActiveCircleMember, IsAdminOrMembershipOwner]
        return [p() for p in permissions]

    
    def get_queryset(self):
        """Returns circle members"""
        return Membership.objects.filter(circle=self.circle, is_active=True)


    def get_object(self):
        """Return Circle member by users username."""
        return get_object_or_404(Membership, user__username=self.kwargs['pk'], circle=self.circle, is_active=True)
    

    def perfom_destroy(self, instance):
        """Disable membership"""
        instantce.is_active = False
        instance.save()


