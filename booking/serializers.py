from rest_framework import serializers
from .models import Category, Property, Booking


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий объектов."""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class PropertySerializer(serializers.ModelSerializer):
    """Сериализатор для объектов аренды."""
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'category', 'category_detail', 'title',
            'description', 'capacity', 'price_per_hour', 'is_active'
        ]


class BookingSerializer(serializers.ModelSerializer):
    """Сериализатор для бронирований."""
    user = serializers.ReadOnlyField(source='user.username')
    property_title = serializers.ReadOnlyField(source='property.title')

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'property', 'property_title',
            'start_time', 'end_time', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['status', 'total_price', 'created_at']

    def validate(self, attrs):
        """Проверка корректности дат бронирования."""
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                {"end_time": "Время окончания должно быть позже времени начала."}
            )

        return attrs