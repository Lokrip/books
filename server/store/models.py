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