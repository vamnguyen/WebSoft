from rest_framework import serializers
from ..models.book import BookType, Author, Book

class BookTypeSerializer(serializers.Serializer):
    bookTypeName = serializers.CharField()

class AuthorSerializer(serializers.Serializer):
    authorName = serializers.CharField(max_length=255)


class BookSerializer(serializers.Serializer):
    bookName = serializers.CharField()
    bookTypeId = serializers.IntegerField()
    authorId = serializers.IntegerField()
    quantity = serializers.IntegerField()