from django.urls import reverse    

from rest_framework.test import APITestCase
from rest_framework import status

from store.models import Book
from store.serializer import BooksSerializer

class BooksApiTestCase(APITestCase):
    def test_get(self):
        # Django автоматически создает базу данных с таблицей Book,
        # затем добавляет туда данные, а по окончании теста удаляет базу данных с таблицами.
        book1 = Book.objects.create(name="Test book 1", price=25)
        book2 = Book.objects.create(name="Test book 1", price=55)
        
        #через reverse мы берем name="book-list" тоесть имя маршрута
        #например path("api/books", book_list, name="book-list") берем name
        url = reverse("book-list")
        response = self.client.get(url)
        
        serializer = BooksSerializer([book1, book2], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)