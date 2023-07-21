from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_ok(self):
        self.user = User.objects.create_user(username='test_username')
        book_1 = Book.objects.create(name='Test book 1', price=25,
                                     author_name='Test author 1', owner=self.user)
        book_2 = Book.objects.create(name='Test book 2', price=35.01,
                                     author_name='Test author 2', owner=self.user)
        data = BooksSerializer([book_1, book_2], many=True).data
        self.client.force_login(self.user)
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Test author 1',
                'owner': self.user.id
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '35.01',
                'author_name': 'Test author 2',
                'owner': self.user.id
            },
        ]
        self.assertEqual(expected_data, data)
