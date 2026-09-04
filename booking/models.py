
# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Category(models.Model):
    """Категории объектов (Дом, Баня, Беседка)."""
    name = models.CharField("Название категории", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Property(models.Model):
    """Объект аренды."""
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name="properties",
        verbose_name="Категория"
    )
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    capacity = models.PositiveIntegerField("Вместимость (человек)")
    price_per_hour = models.DecimalField("Цена за час (руб.)", max_digits=10, decimal_places=2)
    is_active = models.BooleanField("Доступен для бронирования", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Объект аренды"
        verbose_name_plural = "Объекты аренды"

    def __str__(self):
        return f"{self.title} ({self.category.name})"


class Booking(models.Model):
    """Модель бронирования."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает подтверждения'
        CONFIRMED = 'confirmed', 'Подтверждено'
        CANCELLED = 'cancelled', 'Отменено'
        COMPLETED = 'completed', 'Завершено'

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="bookings",
        verbose_name="Пользователь"
    )
    property = models.ForeignKey(
        Property, 
        on_delete=models.CASCADE, 
        related_name="bookings",
        verbose_name="Объект"
    )
    start_time = models.DateTimeField("Время начала")
    end_time = models.DateTimeField("Время окончания")
    total_price = models.DecimalField("Итоговая стоимость", max_digits=10, decimal_places=2, blank=True)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField("Дата создания брони", auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-created_at']

    def __str__(self):
        return f"Бронь #{self.id} — {self.property.title} ({self.user.username})"

    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("Время окончания должно быть позже времени начала.")