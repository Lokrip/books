from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin

from rest_framework.viewsets import (
    ModelViewSet,
    GenericViewSet
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from store.permissions import IsOwnerOrStaffOrReadOnly

from store.models import (
    Book,
    UserBookRelation
)
from store.serializer import (
    BooksSerializer,
    UserBookRelationSerializer
)


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
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def perform_create(self, serializer):
        #validated_data это те данные каторый приходят после успешной валидаций
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = "book"

    #Он находиться внутри UpdateModelMixin в методе update instance = self.get_object()
    def get_object(self):
        assert self.lookup_field in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, self.lookup_field)
        )
        
        obj, created = UserBookRelation.objects.get_or_create(
            user=self.request.user,
            book_id=self.kwargs["book"]
        )
        return obj


def auth(request):
    return render(request, "oauth.html")