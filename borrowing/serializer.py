from .models import Borrowing
from rest_framework import serializers


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"

        read_only_fields = ['id','user', 'borrow_date']