from django.urls import path, include
from .views import BookListView, BookDetailView, AuthorView, CategoryView


urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorView.as_view(), name='author-list'),
    path('categories/', CategoryView.as_view(), name='category-list'),
]