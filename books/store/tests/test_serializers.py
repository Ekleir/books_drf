from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create_user(username='test_username1', first_name='Ivan', last_name='Ivanov')
        user2 = User.objects.create_user(username='test_username2', first_name='Petr', last_name='Petrov')
        user3 = User.objects.create_user(username='test_username3', first_name='1', last_name='2')

        book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Test author 1', owner=user1)
        book_2 = Book.objects.create(name='Test book 2', price=35.01, author_name='Test author 2')

        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=5)
        user_book_3 = UserBookRelation.objects.create(user=user3, book=book_1, like=True, rate=4)

        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=False)
        UserBookRelation.objects.create(user=user3, book=book_2, like=True, rate=4)

        book = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).order_by('id')
        data = BooksSerializer(book, many=True).data
        self.client.force_login(user1)
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Test author 1',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'test_username1',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Ivanov',
                    },
                    {
                        'first_name': 'Petr',
                        'last_name': 'Petrov',
                    },
                    {
                        'first_name': '1',
                        'last_name': '2',
                    }
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '35.01',
                'author_name': 'Test author 2',
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Ivanov',
                    },
                    {
                        'first_name': 'Petr',
                        'last_name': 'Petrov',
                    },
                    {
                        'first_name': '1',
                        'last_name': '2',
                    }
                ]
            },
        ]
        self.assertEqual(expected_data, data)

