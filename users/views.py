import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import random
from . import serializers, models
from django.core.mail import send_mail

class RegisterView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password'),
            is_active=False
        )

        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        models.ConfirmUser.objects.create(code=code, user=user)

        send_mail(
            'Registration code',
            message=f'Your registration code is: {code}',
            from_email='<EMAIL>',
            recipient_list=[user.email],
        )

        return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)


class AuthAPIView(APIView):
    def post(self, request):
        serializer = serializers.AuthSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Invalid credentials'})


class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = serializers.ConfirmUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sms_code_value = serializer.validated_data.get('sms_code')
        try:
            sms_code = models.ConfirmUser.objects.get(code=sms_code_value)
        except models.ConfirmUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Code not found'})

        sms_code.user.is_active = True
        sms_code.user.save()
        sms_code.delete()

        return Response(status=status.HTTP_200_OK)


