"""User models admin"""

#django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#Models
from cride.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """User model Admin"""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client')
    list_filter = ('is_client', 'is_staff', 'created', 'modified')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile Model Admin"""

    list_display = ('user', 'reputation', 'rides_taken', 'rides_offered')
    search_fields = ('user__username',  'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('reputation',)

admin.site.register(User, CustomUserAdmin)
