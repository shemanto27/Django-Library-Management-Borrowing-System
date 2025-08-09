from rest_framework import serializers
from .models import BorrowModel

class BorrowSerializer(serializers.ModelSerializer):

    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BorrowModel
        fields = ['id', 'book_id', 'borrow_date', 'due_date', 'return_date']
        read_only_fields = ['id', 'borrow_date', 'due_date', 'return_date']

class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowModel
        fields = ['id', 'return_date']