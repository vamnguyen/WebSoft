
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from django.core.serializers import serialize
from django.forms.models import model_to_dict
from ..serializers.book import BookTypeSerializer, AuthorSerializer, BookSerializer
from ..models import BookType, Author, Book, Parameter

from ..messages.book import BookMessage

class GetBookType(GenericAPIView):
    serializer_class = BookTypeSerializer
    queryset = BookType.objects.all()

    def get(self, request):
        queryset = BookType.objects.all()

        bookTypeData = {}
        for bookType in queryset:
            bookTypeData[bookType.BookTypeId] = model_to_dict(bookType)

        return Response({
                "success": True,
                "message": BookMessage.MSG1001,
                "data": bookTypeData
            }, status=status.HTTP_200_OK)
    
class GetBookTypeWithId(GenericAPIView):
    serializer_class = BookTypeSerializer
    queryset = BookType.objects.all()

    def get(self, request, id):
        try:
            queryset = BookType.objects.get(pk=id)
        except BookType.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG1002
                }
            )  
        return Response({
                "success": True,
                "message": BookMessage.MSG1001,
                "data": model_to_dict(queryset)
            }, status=status.HTTP_200_OK)
    
class GetAuthor(GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get(self, request):
        queryset = Author.objects.all()

        authorData = {}
        for author in queryset:
            authorData[author.AuthorId] = model_to_dict(author)

        return Response({
                "success": True,
                "message": BookMessage.MSG2001,
                "data": authorData
            }, status=status.HTTP_200_OK)
    
class GetAuthorWithId(GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get(self, request, id):
        try:
            queryset = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG2002
                }
            )  
        return Response({
                "success": True,
                "message": BookMessage.MSG2001,
                "data": model_to_dict(queryset)
            }, status=status.HTTP_200_OK)

class GetBook(GenericAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request):
        queryset = Book.objects.all()

        bookData = {}
        for book in queryset:
            bookData[book.BookId] = model_to_dict(book)

        return Response({
                "success": True,
                "message": BookMessage.MSG3001,
                "data": bookData
            }, status=status.HTTP_200_OK)
    
class GetBookWithId(GenericAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request, id):
        try:
            queryset = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG3002
                }
            )  
        return Response({
                "success": True,
                "message": BookMessage.MSG3001,
                "data": model_to_dict(queryset)
            }, status=status.HTTP_200_OK)
    
class AddBookTypeAPIVIew(GenericAPIView):
    serializer_class = BookTypeSerializer
    queryset = BookType.objects.all()

    def get(self, request):
        queryset = BookType.objects.all()

        bookTypeData = {}
        for bookType in queryset:
            bookTypeData[bookType.BookTypeId] = model_to_dict(bookType)

        return Response({
                "success": True,
                "message": BookMessage.MSG1001,
                "data": bookTypeData
            }, status=status.HTTP_200_OK)
    
    def post(self, request):
        bookTypeData = BookTypeSerializer(data=request.data)

        if not bookTypeData.is_valid(raise_exception=True):
            return Response({
                "success": False,
                "message": BookMessage.MSG1004
            }, status=status.HTTP_400_BAD_REQUEST)
        
        bookTypeName = bookTypeData.data['bookTypeName']
        
        if (bookTypeName is None):
            return Response({
                "success": False,
                "message": BookMessage.MSG1009
            }, status=status.HTTP_400_BAD_REQUEST)
        
        maxNameLength = Parameter.objects.filter(ParameterName='MaxNameLength').first()
        minBNameLength = Parameter.objects.filter(ParameterName='MinNameLength').first()

        if (len(bookTypeName) < minBNameLength.Value or
            len(bookTypeName) > maxNameLength.Value):
            return Response({
                "success": False,
                "message": BookMessage.MSG1010
            }, status=status.HTTP_400_BAD_REQUEST)

        BookType(BookTypeName = bookTypeName).save()

        return Response({
                "success": True,
                "message": BookMessage.MSG1003,
                "data": bookTypeData.data,
            }, status=status.HTTP_200_OK)


class AddAuthorViewAPI(GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get(self, request):
        queryset = Author.objects.all()

        authorData = {}
        for author in queryset:
            authorData[author.AuthorId] = model_to_dict(author)

        return Response({
                "success": True,
                "message": BookMessage.MSG2001,
                "data": authorData
            }, status=status.HTTP_200_OK)

    def post(self, request):
        authorData = AuthorSerializer(data=request.data)
        
        if not authorData.is_valid(raise_exception=True):
            return Response({
                "success": False,
                "message": BookMessage.MSG2004
            }, status=status.HTTP_400_BAD_REQUEST)
        
        authorName = authorData.data['authorName']

        if (authorName is None):
            return Response({
                "success": False,
                "message": BookMessage.MSG2009
            }, status=status.HTTP_400_BAD_REQUEST)
        
        maxNameLength = Parameter.objects.filter(ParameterName='MaxNameLength').first()
        minBNameLength = Parameter.objects.filter(ParameterName='MinNameLength').first()

        if (len(authorName) < minBNameLength.Value or
            len(authorName) > maxNameLength.Value):
            return Response({
                "success": False,
                "message": BookMessage.MSG2010
            }, status=status.HTTP_400_BAD_REQUEST)
        
        Author(AuthorName = authorName).save()
            
        return Response({
                "success": True,
                "message": BookMessage.MSG2003,
                "data": authorData.data
            }, status=status.HTTP_200_OK)
    
class AddBookViewAPI(GenericAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request):
        queryset = Book.objects.all()

        bookData = {}
        for book in queryset:
            bookData[book.BookId] = model_to_dict(book)

        return Response({
                "success": True,
                "message": BookMessage.MSG3001,
                "data": bookData
            }, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        bookData = BookSerializer(data=request.data)

        if not bookData.is_valid(raise_exception=True):
            return Response({
                "success": False,
                "message": BookMessage.MSG3004
            }, status=status.HTTP_400_BAD_REQUEST)
        
        bookName = bookData.validated_data['bookName']
        bookTypeId = bookData.validated_data['bookTypeId']
        authorId = bookData.validated_data['authorId']
        
        if (bookName is None or
            bookTypeId is None or
            authorId is None):
            return Response({
                "success": False,
                "message": BookMessage.MSG3009
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            bookType = BookType.objects.get(pk=bookTypeId)
            author = Author.objects.get(pk=authorId)
        except BookType.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG3011
                }
            )
        except Author.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG3012
                }
            )
        
        maxNameLength = Parameter.objects.filter(ParameterName='MaxNameLength').first()
        minBNameLength = Parameter.objects.filter(ParameterName='MinNameLength').first()

        if (len(bookName) < minBNameLength.Value or
            len(bookName) > maxNameLength.Value):
            return Response({
                "success": False,
                "message": BookMessage.MSG3010
            }, status=status.HTTP_400_BAD_REQUEST)
        
        Book(BookName = bookName, BookTypeId = bookType, AuthorId = author).save()

        return Response({
                "success": True,
                "message": BookMessage.MSG3003,
                "data": bookData.data
            }, status=status.HTTP_200_OK)

class EditBookTypeViewAPI(GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = BookType.objects.all()

    def get(self, request, id):
        try:
            queryset = BookType.objects.get(pk=id)
        except BookType.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG1002
                }
            )  
        return Response({
                "success": True,
                "message": BookMessage.MSG1001,
                "data": model_to_dict(queryset)
            }, status=status.HTTP_200_OK)

    def put(self, request, id):
        bookTypeData = BookTypeSerializer(data=request.data)

        try:
            queryset = BookType.objects.get(pk=id)
        except BookType.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG1002
                }
            )  
        
        if not bookTypeData.is_valid(raise_exception=True):
            return Response({
                "success": False,
                "message": BookMessage.MSG1006
            }, status=status.HTTP_400_BAD_REQUEST)
        
        bookTypeName = bookTypeData.data['bookTypeName']
        if (bookTypeName is None):
            return Response({
                "success": False,
                "message": BookMessage.MSG1009
            }, status=status.HTTP_400_BAD_REQUEST)
        
        maxNameLength = Parameter.objects.filter(ParameterName='MaxNameLength').first()
        minBNameLength = Parameter.objects.filter(ParameterName='MinNameLength').first()

        if (len(bookTypeName) < minBNameLength.Value or
            len(bookTypeName) > maxNameLength.Value):
            return Response({
                "success": False,
                "message": BookMessage.MSG1010
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset.BookTypeName = bookTypeName
        queryset.save()
            
        return Response({
                "success": True,
                "message": BookMessage.MSG1005,
                "data": bookTypeData.data
            }, status=status.HTTP_200_OK)
       
class EditAuthorViewAPI(GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get(self, request, id):
        try:
            queryset = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG2002
                }
            )
        authorName = queryset.AuthorName
        return Response({
            "success": True,
            "message": BookMessage.MSG2001,
            "data": {
                "authorName": authorName,
            }
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        authorData = AuthorSerializer(data=request.data)
        try:
            queryset = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG2002
                }
            )  
        
        if not authorData.is_valid(raise_exception=True):
            return Response({
                "success": False,
                "message": BookMessage.MSG2006
            }, status=status.HTTP_400_BAD_REQUEST)
        
        authorName = authorData.data['authorName']

        if (authorName is None):
            return Response({
                "success": False,
                "message": BookMessage.MSG2009
            }, status=status.HTTP_400_BAD_REQUEST)
        
        maxNameLength = Parameter.objects.filter(ParameterName='MaxNameLength').first()
        minBNameLength = Parameter.objects.filter(ParameterName='MinNameLength').first()

        if (len(authorName) < minBNameLength.Value or
            len(authorName) > maxNameLength.Value):
            return Response({
                "success": False,
                "message": BookMessage.MSG2010
            }, status=status.HTTP_400_BAD_REQUEST)
        
        queryset.save()
            
        return Response({
                "success": True,
                "message": BookMessage.MSG2005,
                "data": {
                    "authorName": authorName
                }
            }, status=status.HTTP_200_OK)
    
class EditBookViewAPI(GenericAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request, id):
        try:
            queryset = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG3002
                }
            )  
        return Response({
                "success": True,
                "message": BookMessage.MSG3001,
                "data": model_to_dict(queryset)
            }, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        bookData = BookSerializer(data=request.data)

        try:
            queryset = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG3002
                }
            )  
        
        if not bookData.is_valid(raise_exception=True):
            return Response({
                "success": False,
                "message": BookMessage.MSG3006
            }, status=status.HTTP_400_BAD_REQUEST)
              
        bookName = bookData.validated_data['bookName']
        bookTypeId = bookData.validated_data['bookTypeId']
        authorId = bookData.validated_data['authorId']
        
        if (bookName is None or
            bookTypeId is None or
            authorId is None):
            return Response({
                "success": False,
                "message": BookMessage.MSG3009
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            bookType = BookType.objects.get(pk=bookTypeId)
            author = Author.objects.get(pk=authorId)
        except BookType.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG3011
                }
            )
        except Author.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG3012
                }
            )

        maxNameLength = Parameter.objects.filter(ParameterName='MaxNameLength').first()
        minBNameLength = Parameter.objects.filter(ParameterName='MinNameLength').first()

        if (len(bookName) < minBNameLength.Value or
            len(bookName) > maxNameLength.Value):
            return Response({
                "success": False,
                "message": BookMessage.MSG3010
            }, status=status.HTTP_400_BAD_REQUEST)
            
        queryset.BookName = bookName
        queryset.BookTypeId = bookType
        queryset.AuthorId = author
        
        queryset.save()

        return Response({
                "success": True,
                "message": BookMessage.MSG3005,
                "data": bookData.data
            }, status=status.HTTP_200_OK)

class DeleteBookTypeViewAPI(GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = BookType.objects.all()

    def get(self, request):
        try:
            queryset = BookType.objects.get(pk=id)
        except BookType.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG1002
                }
            )  
        return Response({
                "success": True,
                "message": BookMessage.MSG1001,
                "data": model_to_dict(queryset)
            }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            queryset = BookType.objects.get(pk=id)
        except BookType.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG1002
                }
            )  

        queryset.delete()
            
        return Response({
                "success": True,
                "message": BookMessage.MSG1007,
            }, status=status.HTTP_200_OK)
    
class DeleteAuthorViewAPI(GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get(self, request):
        try:
            queryset = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG2002
                }
            )  
        return Response({
                "success": True,
                "message": BookMessage.MSG2001,
                "data": model_to_dict(queryset)
            }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            queryset = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG2002
                }
            )  

        queryset.delete()
            
        return Response({
                "success": True,
                "message": BookMessage.MSG2007,
            }, status=status.HTTP_200_OK)
    
class DeleteBookViewAPI(GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = Book.objects.all()

    def get(self, request):
        try:
            queryset = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG3002
                }
            )  
        return Response({
                "success": True,
                "message": BookMessage.MSG3001,
                "data": model_to_dict(queryset)
            }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            queryset = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": BookMessage.MSG3002
                }
            )  

        queryset.delete()
            
        return Response({
                "success": True,
                "message": BookMessage.MSG3007,
            }, status=status.HTTP_200_OK)
    