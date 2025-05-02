from rest_framework import serializers
from store.models import (
    Book,
    UserBookRelation
)

from django.contrib.auth.models import User


class BookReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


class BooksSerializer(serializers.ModelSerializer):
    # likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(
        max_digits=3, 
        decimal_places=2,
        read_only=True
    )
    owner_name = serializers.CharField(source="owner.username", default="Anonymous", read_only=True)
    readers = BookReaderSerializer(many=True, read_only=True)
    
    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()
    
    class Meta:
        model = Book
        fields = ("id", "name", "price", "author_name", 
                  "annotated_likes", "rating", "owner_name", "readers")


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ("book", "like", "in_bookmarks", "rate")
