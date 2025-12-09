from django.contrib import admin
from .models import Borrowing

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "borrow_date", "return_date", "status")
    list_filter = ("status", "borrow_date", "return_date")
    search_fields = ("book__title",)
    ordering = ("-borrow_date",)