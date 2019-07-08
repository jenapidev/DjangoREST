"""Circle views"""

#django rest-framework
from rest_framework import mixins, viewsets

#permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.circles import IsCircleAdmin

#filter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

#serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Circle View Set"""
    
    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'

    #Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slug_name', 'name', 'about')
    ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'members_limit')
    ordering = ('-members__count', '-rides_offered', '-rides_taken')
    filter_fields = ('verified', 'is_limited')


    def get_queryset(self):
        """Restrict list of circles to only publics"""

        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset
    

    def get_permissions(self):
        """Asign Permissions based on actions"""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]


    def perform_create(self, serializer):
        """Assign a Circle admin"""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )
