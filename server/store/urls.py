from django.urls import path, include

from rest_framework.routers import SimpleRouter

from store.views import BookViewSet

router = SimpleRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("", include(router.urls))
]
