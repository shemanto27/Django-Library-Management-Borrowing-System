from rest_framework import serializers
from .models import BorrowModel

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowModel
        fields = '__all__'

class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowModel
        fields = ['id', 'return_date']