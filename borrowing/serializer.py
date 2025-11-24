from datetime import date

from rest_framework import serializers

from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"

        read_only_fields = ["id", "user", "borrow_date"]

    def validate(self, data):

        user = self.context["request"].user
        book = data.get("book")
        return_date = data.get("return_date")

        if not user.status:
            raise serializers.ValidationError("Usuário inativo no sistema")

        if book is None:
            raise serializers.ValidationError({"book": "Livro é obrigatório."})

        if book.status != "AVAILABLE":
            raise serializers.ValidationError("Livro reservado ou não disponível")

        if return_date is None or return_date <= date.today():
            raise serializers.ValidationError("A data de devolução deve ser posterior à data atual")

        limit_borrowing = Borrowing.objects.filter(user=user).count()
        if limit_borrowing >= 5:
            raise serializers.ValidationError("O limite de empréstimos de livros é 5")

        return data
