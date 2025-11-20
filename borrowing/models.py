from uuid import uuid4

from django.db import models


class Borrowing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, unique=True, editable=False)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, name="user")
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE, name="book")
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
