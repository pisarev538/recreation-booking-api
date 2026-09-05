from rest_framework import viewsets, permissions
from .models import Category, Property, Booking
from .serializers import CategorySerializer, PropertySerializer, BookingSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """API эндпоинт для работы с категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PropertyViewSet(viewsets.ModelViewSet):
    """API эндпоинт для работы с объектами аренды."""
    queryset = Property.objects.filter(is_active=True)
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    """API эндпоинт для работы с бронированиями."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Обычный пользователь видит только свои бронирования, админ — все."""
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        """Автоматическая привязка текущего пользователя к создаваемому бронированию."""
        serializer.save(user=self.request.user)
