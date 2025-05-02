import json

from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.db.models import Count, Case, When, Avg

from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework import status

from store.models import Book, UserBookRelation
from store.serializer import BooksSerializer


class BooksApiTestCase(APITestCase):
    #эта функция запускаеться каждый раз перед тем как запускаешь какойта из наших тестов
    def setUp(self): 
        self.user = User.objects.create(username="test_username")
        # Django автоматически создает базу данных с таблицей Book,
        # затем добавляет туда данные, а по окончании теста удаляет базу данных с таблицами.
        self.book1 = Book.objects.create(owner=self.user, name="Test book 1", price=25, author_name="Author 1")
        self.book2 = Book.objects.create(name="Test book 2", price=55, author_name="Author 5")
        self.book3 = Book.objects.create(name="Test book Author 1", price=55, author_name="Author 2")

        UserBookRelation.objects.create(user=self.user, book=self.book1, like=True,
                                        rate=5)
        
    def test_get(self):
        # # Django автоматически создает базу данных с таблицей Book,
        # # затем добавляет туда данные, а по окончании теста удаляет базу данных с таблицами.
        # book1 = Book.objects.create(name="Test book 1", price=25)
        # book2 = Book.objects.create(name="Test book 1", price=55)

        #через reverse мы берем name="book-list" тоесть имя маршрута
        #например path("api/books", book_list, name="book-list") берем name
        url = reverse("book-list")
        
        
        # мы говрим что после этого запроса self.client.get(url) 
        # у нас должно быть 2 sql запроса
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(2, len(queries))
            
        books = Book.objects.all().annotate(annotated_likes=Count(
                #SELECT book.*, COUNT(CASE WHEN user_book_relation.like = TRUE THEN 1 ELSE NULL END) AS annotated_likes
                #мы делаем такой запрос
                Case(When(user_book_relation__like=True, then=1))), rating=Avg("user_book_relation__rate")).order_by("pk")
        serializer = BooksSerializer(books, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

        for i in range(len(serializer.data)):
            if serializer.data[i]['name'] == "Test book 1":
                self.assertEqual(serializer.data[i]['rating'], "5.00")
                self.assertEqual(serializer.data[i]['annotated_likes'], 1)
            else:
                self.assertEqual(serializer.data[i]['rating'], None)
                self.assertEqual(serializer.data[i]['annotated_likes'], 0)
                

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse("book-list")
        data = {
            "name": "Programming in Python 3",
            "price": 150,
            "author_name": "Mark Summerfield"
        }
        json_data = json.dumps(data)
        #аутенфицируем пользователя в системе когда делаем запрос на сервер
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse("book-detail", args=(self.book1.id,))
        data = {
            "name": self.book1.name,
            "price": 575,
            "author_name": self.book1.author_name
        }
        json_data = json.dumps(data)
        #аутенфицируем пользователя в системе когда делаем запрос на сервер
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        #после обновления делаем refresh текущей книги тоесть записи и она становиться обновленной иза запроса put
        self.book1.refresh_from_db()
        self.assertEqual(f"{575:.2f}", response.data.get("price"))
        self.assertEqual(575, self.book1.price)

    def test_delete(self):
        book_id = self.book1.id
        url = reverse("book-detail", args=(book_id,))
        self.client.force_login(self.user)
        response = self.client.delete(url, content_type="application/json")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Book.objects.filter(id=book_id).exists())

    def test_get_filter(self):
        #через reverse мы берем name="book-list" тоесть имя маршрута
        #например path("api/books", book_list, name="book-list") берем name
        url = reverse("book-list")
        response = self.client.get(url, data={"search": "Author 1"})
        books = Book.objects.filter(id__in=[self.book1.pk, self.book3.pk]).annotate(annotated_likes=Count(
                #SELECT book.*, COUNT(CASE WHEN user_book_relation.like = TRUE THEN 1 ELSE NULL END) AS annotated_likes
                #мы делаем такой запрос
                Case(When(user_book_relation__like=True, then=1))), rating=Avg("user_book_relation__rate")).order_by('pk')
        serializer = BooksSerializer(books, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    #Негативный тест
    def test_update_not_owner(self):
        self.user2 = User.objects.create(username="test_username2")
        url = reverse("book-detail", args=(self.book1.id,))
        data = {
            "name": self.book1.name,
            "price": 575,
            "author_name": self.book1.author_name
        }
        json_data = json.dumps(data)
        #аутенфицируем пользователя в системе когда делаем запрос на сервер
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        #после обновления делаем refresh текущей книги тоесть записи и она становиться обновленной иза запроса put
        self.book1.refresh_from_db()
        self.assertEqual({'detail': ErrorDetail(
            string='You do not have permission to perform this action.', 
            code='permission_denied'
        )}, response.data)
        self.assertEqual(25, self.book1.price)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username="test_username2",
                                         is_staff=True)
        url = reverse("book-detail", args=(self.book1.id,))
        data = {
            "name": self.book1.name,
            "price": 575,
            "author_name": self.book1.author_name
        }
        json_data = json.dumps(data)
        #аутенфицируем пользователя в системе когда делаем запрос на сервер
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        #после обновления делаем refresh текущей книги тоесть записи и она становиться обновленной иза запроса put
        self.book1.refresh_from_db()
        self.assertEqual(575, self.book1.price)


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.user2 = User.objects.create(username="test_username2")
        self.book1 = Book.objects.create(owner=self.user, name="Test book 1", price=25, author_name="Author 1")
        self.book2 = Book.objects.create(name="Test book 2", price=55, author_name="Author 5")

    def test_like(self):
        url = reverse("userbookrelation-detail", args=(self.book1.id,))
        data = {"like": True}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)
        self.assertTrue(relation.like)
        
        data = {
            "in_bookmarks": True,
        }
        
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)
        self.assertTrue(relation.in_bookmarks)
        
    def test_rate(self):
        url = reverse("userbookrelation-detail", args=(self.book1.id,))
        data = {"rate": 3}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)
        self.assertEqual(3, relation.rate)
        
    def test_wrong(self):
        url = reverse("userbookrelation-detail", args=(self.book1.id,))
        data = {"rate": 6}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        #трейтий аргумент assertEqual это какой сделать принт если эта штука не сошлась не совпала
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)