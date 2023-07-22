from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    """Book model"""
    name = models.CharField('Название', max_length=255)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    author_name = models.CharField('Автор', max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, related_name='my_books', verbose_name='Владелец')
    readers = models.ManyToManyField(User, through='UserBookRelation',
                                     related_name='books', verbose_name='Читатели')

    def __str__(self):
        return f'Id {self.id}: {self.name}'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class UserBookRelation(models.Model):
    """UserBookRelation model"""
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    like = models.BooleanField('Нравится', default=False)
    in_bookmarks = models.BooleanField('В закладках', default=False)
    rate = models.PositiveSmallIntegerField('Рейтинг', choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.book.name}, RATE {self.rate}'

