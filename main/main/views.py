from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from main.serializers import LoginSerializer


class LoginView(APIView):
    """Представление авторизации пользователя"""
    serializer_class = LoginSerializer

    def post(self, request, *awgs, **kwargs):
        serializer = LoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if not user:
                return Response({'error': 'неправильное имя пользователя или пароль'}, status=HTTP_404_NOT_FOUND)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)

        