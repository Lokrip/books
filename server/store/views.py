from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from store.models import Book
from store.serializer import BooksSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    #тут мы указываем класс фильтра
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Указываем поля, доступные для фильтрации
    filterset_fields = ['price']
    # поля каторый будут использоваться в пойске
    search_fields = ['name', 'author_name']
    # поля каторые будут сортироваться
    ordering_fields = ['price', 'author_name']
    permission_classes = [IsAuthenticated]
    
    
def auth(request):
    return render(request, "oauth.html")