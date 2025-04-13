from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    #без related_name будет конфликт то что User не понимает
    #в какой книге он owner а в какой книге он читатель так что надо добавить related_name
    #а не использовать стандарт как book_set его можно использовать если у нас одна связь к модели
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                              related_name="my_books")
    # Оно хранит всех пользователей, 
    # которые каким-либо образом связаны с книгой 
    # (например, лайкнули, добавили в закладки, оценили).
    readers = models.ManyToManyField(User, through="UserBookRelation", 
                                     related_name="books")
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
        return "Id %s: %s" % (self.id, self.name)
    
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
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="user_book_relation")
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    
    def __str__(self):
        return "%s: %s, RATE %s" % (
            self.user.username,
            self.book.name,
            self.rate
        )