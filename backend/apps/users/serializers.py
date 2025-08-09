from rest_framework import serializers
from .models import User

class UserPenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'penalty_points']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'penalty_points']
        read_only_fields = ['id', 'penalty_points']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }