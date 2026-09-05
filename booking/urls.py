from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PropertyViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]