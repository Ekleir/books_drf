import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_username')
        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=55,
                                          author_name='Author 5', owner=self.user)
        self.book_3 = Book.objects.create(name='Test book Author 1',
                                          price=55, author_name='Author 2', owner=self.user)

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_id(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        response = self.client.get(url)
        serializer_data = BooksSerializer(self.book_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 55})
        serializer_data = BooksSerializer([self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_sorted(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': '-author_name'})
        serializer_data = BooksSerializer([self.book_2, self.book_3, self.book_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(Book.objects.all().count(), 3)
        url = reverse('book-list')
        data = {
            'name': 'Test book 3',
            'price': 150,
            'author_name': 'Author 3'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Book.objects.all().count(), 4)
        self.assertEqual(Book.objects.last().owner, self.user)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 575,
            'author_name': self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.price, 575)

    def test_update_not_owner(self):
        self.user2 = User.objects.create_user(username='test_username2')
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 575,
            'author_name': self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(response.data,
                         {'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}
                         )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.price, 25)

    def test_delete(self):
        self.assertEqual(Book.objects.all().count(), 3)
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Book.objects.all().count(), 2)
        self.assertRaises(Book.DoesNotExist, Book.objects.get, id=self.book_1.id)

    def test_delete_not_owner(self):
        self.user2 = User.objects.create_user(username='test_username2')
        self.assertEqual(Book.objects.all().count(), 3)
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Book.objects.all().count(), 3)
        self.assertEqual(self.book_1, Book.objects.get(id=self.book_1.id))

    def test_update_not_owner_but_stuff(self):
        self.user2 = User.objects.create_user(username='test_username2',
                                              is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 575,
            'author_name': self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.price, 575)


class BooksRelationApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_username')
        self.user2 = User.objects.create_user(username='test_username2')
        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=55,
                                          author_name='Author 5', owner=self.user)

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.like)

        data = {
            'in_bookmarks': True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            'rate': 2,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(relation.rate, 2)

    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            'rate': 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
