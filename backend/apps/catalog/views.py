from  .models import BookModel, AuthorModel, CategoryModel
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class BookListView(APIView):
    """
    GET: List books (with optional filters)
    POST: Create book (admin only)
    """
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request):
        books = BookModel.objects.all()
        serializer = BookSerializer(books, many=True)

        # applying author and category filters
        author_name = request.query_params.get('author_name')
        category_name = request.query_params.get('category_name')

        if author_name:
            books = books.filter(author__name__icontains=author_name)
        if category_name:
            books = books.filter(category__name__icontains=category_name)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=BookSerializer)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    """
    GET: Retrieve single book
    PUT: Update book (admin only)
    DELETE: Delete book (admin only)
    """
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request, id):
        book = get_object_or_404(BookModel, id=id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BookSerializer)
    def put(self, request, id):
        book = get_object_or_404(BookModel, id=id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    @swagger_auto_schema(operation_description="Delete a book")
    def delete(self, request, id):
        book = get_object_or_404(BookModel, id=id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorView(APIView):
    """
    GET: List authors
    POST: Create author (admin only)
    """
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


    def get(self, request):
        authors = AuthorModel.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=AuthorSerializer)
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryView(APIView):
    """
    GET: List categories
    POST: Create category (admin only)
    """
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request):
        categories = CategoryModel.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)