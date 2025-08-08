from django.urls import path, include
from .views import UserView

urlpatterns = [
    path('users/<int:id>/penalties/', UserView.as_view(), name='user'),
]