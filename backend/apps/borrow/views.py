from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class BorrowView(APIView):

    def get(self, request):
        pass
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        pass
        return Response(status=status.HTTP_201_CREATED)
    
class ReturnView(APIView):

    def post(self, request):
        pass
        return Response(status=status.HTTP_201_CREATED)
