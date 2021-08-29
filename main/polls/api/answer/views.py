from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from polls.api.answer.serializers import CreateAnswerSerializer, ViewAnswerSerializer
from polls.service import create_answer


class CreateAnswer(APIView):
    """Сохранение ответа на вопрос"""
    serializer_class = CreateAnswerSerializer
    
    def post(self, request, *args, **kwargs):
        create_serializer = CreateAnswerSerializer(data=request.POST)
        if create_serializer.is_valid():
            create_answer(**create_serializer.data)
            return Response(data=create_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
