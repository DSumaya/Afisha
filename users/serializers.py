from django.contrib.auth.models import User
from rest_framework import serializers



class RegisterSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    conform_password = serializers.CharField(min_length=6)

    def validate(self, data):
        if data['password'] != data['conform_password']:
            raise serializers.ValidationError('Password d0 not match')
        return data

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username ias already')
        return username

class AuthSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(min_length=6)


class ConfirmUserSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(max_length=6)


