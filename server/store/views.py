from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from store.permissions import IsOwnerOrReadOnly

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
    permission_classes = [IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        #validated_data это те данные каторый приходят после успешной валидаций
        serializer.validated_data['owner'] = self.request.user
        serializer.save()
    
def auth(request):
    return render(request, "oauth.html")