from django.urls import path, include
from .views import BorrowView, ReturnView

urlpatterns = [
    path('borrow/', BorrowView.as_view(), name='borrow'),
    path('return/', ReturnView.as_view(), name='return'),
]