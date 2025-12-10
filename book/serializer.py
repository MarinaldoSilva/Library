from rest_framework import serializers

from author.models import Author

from .models import Book

 
class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"

"""
Recebe um Author e aninha na resposta json.
todo o conteúdo do Author é recebido na váriavel 'author_data', e na resposta json mostra os dados do author
esse campo só faz a leitura graças ao read_only=True, os dados são buscados no 'source = Author', nos fileds retornamos tudo, mas poderiamos retornar somente os dados que queremos como o author_data.
OBS: O campo author_data não esta presente na model, só existe no serializer e o seu resultado pode ser eutilizado em outras partes do código
"""

class BookSerializer(serializers.ModelSerializer):

    author_data = AuthorSerializer(source="author", read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

        read_only_fields = ("id",)

class BookBulkSerializer(serializers.ModelSerializer):
    class Meta:

        model = Book
        fields = "__all__"

        read_only_fields = ('id',)#somente leiruta, ignora no POST 

        def create(self, validated_data):
            books_para_criar = []

            for books in validated_data:
                #crianmos instancias de Book e salvamos na lista books_para_criar=[]
                books_para_criar.append(Book(**books))
            
            #lista com os objetos criados
            return Book.objects.bulk_create(books_para_criar)
