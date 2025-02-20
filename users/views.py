from  rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from users.serializers import RegisterSerializers, AuthSerializers, ConfirmUserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


"""Подтверждение регистрации пользователя"""
@api_view(['POST'])
def confirm_user(request):
    serializer = ConfirmUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')
    is_active = serializer.validated_data.get('is_active')
    user = User.objects.create_user(username=username, password=password, is_active=is_active)

    return Response(data=ConfirmUserSerializer(user).data,
                    status=status.HTTP_400_BAD_REQUEST,)

    # return Response(serializer.validated_data, status=status.HTTP_200_OK)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""Авторизация"""
@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User credentials are wrong!'})


"""Регистрация"""
@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.create_user(username=username, password=password)

    return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id})
