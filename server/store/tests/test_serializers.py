from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

from store.models import Book, UserBookRelation
from store.serializer import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username="user1", first_name="Ivan", last_name="Petrov")
        user2 = User.objects.create(username="user2", first_name="Ivan", last_name="Sidorov")
        user3 = User.objects.create(username="user3", first_name="1", last_name='2')
        
        book1 = Book.objects.create(name="Test book 1", price=25, author_name="Author 1", owner=user1)
        book2 = Book.objects.create(name="Test book 1", price=55, author_name="Author 2")

        UserBookRelation.objects.create(user=user1, book=book1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user2, book=book1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user3, book=book1, like=True,
                                        rate=4)
        
        UserBookRelation.objects.create(user=user1, book=book2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user2, book=book2, like=True,
                                        rate=4)
        
        UserBookRelation.objects.create(user=user3, book=book2, like=False)
        
        books = Book.objects.all().annotate(
            annotated_likes=Count(
                #SELECT book.*, COUNT(CASE WHEN user_book_relation.like = TRUE THEN 1 ELSE NULL END) AS annotated_likes
                #мы делаем такой запрос
                Case(When(user_book_relation__like=True, then=1))),
            rating=Avg("user_book_relation__rate")).order_by('id')
        serializer = BooksSerializer(books, many=True)
        expected_data = [
            {
                'id': book1.id,
                'name': "Test book 1",
                'price': "25.00",
                'author_name': "Author 1",
                "annotated_likes": 3,
                "rating": "4.67",
                "owner_name": "user1",
                "readers": [
                    {
                        "username": "user1",
                        "first_name": "Ivan",
                        "last_name": "Petrov"
                    },
                    {
                        "username": "user2",
                        "first_name": "Ivan",
                        "last_name": "Sidorov"
                    },
                    {
                        "username": "user3",
                        "first_name": "1",
                        "last_name": "2"
                    }
                ]
            },
            {
                'id': book2.id,
                'name': "Test book 1",
                'price': "55.00",
                'author_name': "Author 2",
                "annotated_likes": 2,
                "rating": "3.50",
                "owner_name": "Anonymous",
                "readers": [
                    {
                        "username": "user1",
                        "first_name": "Ivan",
                        "last_name": "Petrov"
                    },
                    {
                        "username": "user2",
                        "first_name": "Ivan",
                        "last_name": "Sidorov"
                    },
                    {
                        "username": "user3",
                        "first_name": "1",
                        "last_name": "2"
                    }
                ]
            }
        ]
        self.assertEqual(expected_data, serializer.data)