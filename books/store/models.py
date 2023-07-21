from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    """Книги"""
    name = models.CharField('Название', max_length=255)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    author_name = models.CharField('Автор', max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True)

    def __str__(self):
        return f'Id {self.id}: {self.name}'
