from django.urls import path, include
from .views import UserPenaltyView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('users/<int:id>/penalties/', UserPenaltyView.as_view(), name='user-penalties'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]