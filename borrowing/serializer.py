from rest_framework import serializers

from datetime import date

from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"

        read_only_fields = ["id", "user", "borrow_date"]
        

    def validate(self, data):
        
        user = self.context['request'].user
        book = self.data.get('book')
        return_data = self.data.get('return_date')

        if not user.status:
            raise serializers.ValidationError("Usuário inativo no sistema")
        
        if book.status != 'AVAILABLE' or book.status == 'RESERVED':
            raise serializers.ValidationError("Livro reservado ou não disponível")
        if book.status == 'BORROWED':
            raise serializers.ValidationError('Livro já se encontra emprestado')
        
        if return_data <= date.today():
            raise serializers.ValidationError("A data de devolução não pode ser após a data de emprestimo")
    
        limit_borrowing = Borrowing.objects.filter(user=user).count()
        
        if limit_borrowing >= 5:
            raise serializers.ValidationError("O limite de emprestimos de livros é 5")

        return data