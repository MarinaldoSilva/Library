from .models import Author
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'user', 'name', 'biography', 'birth_date', 'nationality')

        read_only_fields = ['id']

        extra_kwargs = {
            'user':{
                'required':False
            }
        }