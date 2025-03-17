from django.test import TestCase

from store.models import Book
from store.serializer import BooksSerializer

class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name="Test book 1", price=25, author_name="Author 1")
        book2 = Book.objects.create(name="Test book 1", price=55, author_name="Author 2") 
        serializer = BooksSerializer([book1, book2], many=True)
        expected_data = [
            {
                'id': book1.id,
                'name': "Test book 1",
                'price': f"{25:.2f}", 
                'image': None,
                'author_name': "Author 1",
            },
            {
                'id': book2.id,
                'name': "Test book 1",
                'price': f"{55:.2f}",
                'image': None,
                'author_name': "Author 2",
            }
        ]
        self.assertEqual(expected_data, serializer.data)