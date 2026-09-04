
# Register your models here.
from django.contrib import admin
from .models import Category, Property, Booking

admin.site.register(Category)
admin.site.register(Property)
admin.site.register(Booking)