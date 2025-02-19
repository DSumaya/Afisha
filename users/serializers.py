from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import ConfirmUser

class ConfirmUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким именем не найден")

        # Проверяем, существует ли код подтверждения
        try:
            confirmation = ConfirmUser.objects.get(user=user)
        except ConfirmUser.DoesNotExist:
            raise serializers.ValidationError("Код подтверждения не был сгенерирован.")

        # Проверяем, совпадает ли код
        if confirmation.code != data['confirmation_code']:
            raise serializers.ValidationError("Неверный код подтверждения")

        return data



class AuthSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required= True )


class RegisterSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required= True )

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')