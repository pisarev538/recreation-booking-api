from django.db import models

class Author(models.Model):
    """Модель автора"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    """Жанр"""
    name =  models.CharField(max_length=50)

    def __str__(self):
        return self.name
























"""python manage.py makemigrations

python manage.py migrate"""