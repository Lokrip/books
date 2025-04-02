from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, verbose_name="Book Name")
    price = models.DecimalField(
        decimal_places=2, 
        max_digits=9,
        verbose_name="Book Price",
        default=99.99
    )
    image = models.ImageField(
        verbose_name="Book Image", 
        upload_to="books1/images/",
        blank=True,
        null=True
    )
    author_name = models.CharField(max_length=255)

    def __str__(self):
        return "Id %s: %s" % (
            self.id, 
            self.name
        )
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, "Ok"),
        (2, "Fine"),
        (3, "Good"),
        (4, "Amazing"),
        (5, "Incredible")
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)