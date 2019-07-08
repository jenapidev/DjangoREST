"""Rides Urls"""

#django
from django.urls import include, path 

#rest framework 
from rest_framework.routers import DefaultRouter

#views
from .views import rides as rides_views

router = DefaultRouter()
router.register(
    r'circles/(?P<slug_name>[-a-zA-Z0-9_-]+)/rides', 
    rides_views.RideViewSet, 
    basename='ride'
)


urlpatterns = [
    path('', include(router.urls))
]