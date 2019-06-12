"""Circle Admin"""

#django
from django.contrib import admin

#models
from cride.circles.models import Circle

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle admin"""

    list_display = ('slug_name', 'name', 'is_public', 'verified', 'numbers_limit')

    search_fields = ('slug_name', 'name')
    list_filter = ('is_public', 'verified', 'is_limited')
