"""Circles memberships views"""

#Django Rest Framework
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

#Serializers
from cride.circles.serializers.memberships import MembershipModelSerializer
from cride.users.serializers.users import UserModelSerializer

#Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.circles.permissions.memberships import IsAdminOrMembershipOwner


#Models
from cride.circles.models import Circle, Membership, Invitation


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
        """if self.action == 'invitations':
            permissions.append(IsSelfMember)"""
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


    @action(detail=True, methods=['get'])
    def invitations(self, request, *args, **kwargs):
        """Retrieve Members invitations markdown
        return a list containing all the members that have used its invitations and other list with those invitations that have
        not being used yet"""
        member = self.get_object()
        invited_members = Membership.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True
        )

        unused_invitations = Invitation.objects.filter(
            circle=self.circle,
            issued_by=request.user,
            used=False
        ).values_list('code')
        diff = member.remaining_invitations - len(unused_invitations)

        invitations = [x[0] for x in unused_invitations]
        for i in range(0, diff):
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    circle=self.circle
                ).code
            )

        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
            'invitations': invitations
        }
        return Response(data)
