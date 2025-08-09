from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.db import transaction
from django.db.models import F
from django.utils import timezone
from datetime import timedelta

from .models import BorrowModel
from .serializers import BorrowSerializer, ReturnSerializer 
from apps.catalog.models import BookModel

from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class BorrowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=BorrowSerializer)
    def post(self, request):
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({"error": "Book ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user

        # checking borrowing limit of the user
        active_borrow = BorrowModel.objects.filter(user=user, return_date__isnull=True).count()
        if active_borrow >= 3:
            return Response({"error": "You cannot borrow more than 3 books at a time."}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # finding the book availibility and lock it for update
            book = BookModel.objects.select_for_update().filter(id=book_id).first()
            if not book:
                return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
            if book.available_copies <= 0:
                return Response({"error": "No available copies of the book."}, status=status.HTTP_400_BAD_REQUEST)
            

            # updating the book's available copies
            book.available_copies = F('available_copies') - 1
            book.save(update_fields=['available_copies'])
            
            # creating the borrow record
            borrow_record = BorrowModel.objects.create(
                user=user,
                book=book,
                due_date=(timezone.now() + timedelta(days=14)).date()  # Ensure this is a date object
            )

        serializer = BorrowSerializer(borrow_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request):
        user = request.user
        borrow_records = BorrowModel.objects.filter(user=user)
        serializer = BorrowSerializer(borrow_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReturnView(APIView):

    def post(self, request):
        permission_classes = [permissions.IsAuthenticated]
        
        borrow_id = request.data.get('borrow_id')
        if not borrow_id:
            return Response({"error": "Borrow ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        borrow_record = get_object_or_404(BorrowModel, id=borrow_id, user=user)

        # Check if the book is already returned
        if borrow_record.return_date is not None:
            return Response({"error": "This book is already returned."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the book as returned
        borrow_record.return_date = timezone.now()
        borrow_record.save()

        # Update the book's available copies
        with transaction.atomic():
            book = borrow_record.book
            book.available_copies = F('available_copies') + 1
            book.save(update_fields=['available_copies'])

        # check late return
        if borrow_record.due_date and borrow_record.return_date > borrow_record.due_date:
            late_days = (borrow_record.return_date - borrow_record.due_date).days
            
            # adding penalty point
            user.penalty_points += late_days
            user.save(update_fields=['penalty_points'])

        serializer = ReturnSerializer(borrow_record)
        return Response(serializer.data, status=status.HTTP_200_OK)