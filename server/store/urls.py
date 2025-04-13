from django.urls import path, include

from rest_framework.routers import SimpleRouter

from store.views import (
    BookViewSet,
    UserBookRelationViewSet,
    auth
)

router = SimpleRouter()
router.register(r"books", BookViewSet)
router.register(r"book_relation", UserBookRelationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", auth)
]
