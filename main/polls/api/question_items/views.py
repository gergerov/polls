from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from polls.api.question_items.serializers import \
    CreateQuestionItemSerializer, UpdateQuestionItemSerializer, \
    DestroyQuestionItemSerializer, ViewQuestionItemSerializer
from polls.api.question_items.exceptions import QuestionCantContainItems
from polls.models import Question, QuestionItem


class CreateQuestionItem(APIView):
    """Создание варианта ответа на вопрос"""
    permission_classes = [IsAdminUser]
    serializer_class = CreateQuestionItemSerializer

    def post(self, request, *args, **kwargs):
        question_id = request.POST['question']
        question_obj = Question.questions.get(question_id)
        if question_obj.type == 'T':
            raise QuestionCantContainItems
        else:
            ser = CreateQuestionItemSerializer(data=request.POST)
            if ser.is_valid():
                ser.save()
                return Response(data=ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateQuestionItem(UpdateAPIView):
    """Обновление варианта ответа на вопрос"""
    permission_classes = [IsAdminUser]
    serializer_class = UpdateQuestionItemSerializer
    queryset = QuestionItem.objects.all()


class DestroyQuestionItem(DestroyAPIView):
    """Удаление варианта ответа на вопрос"""
    permission_classes = [IsAdminUser]
    serializer_class = DestroyQuestionItemSerializer
    queryset = QuestionItem.objects.all()


class ViewQuestionItem(APIView):
    """Просмотр варианта ответа на вопрос"""
    serializer_class = ViewQuestionItemSerializer
    queryset = QuestionItem.objects.all()

    
    def get(self, request, pk):
        obj = QuestionItem.question_items.get(pk)
        serializer = ViewQuestionItemSerializer(obj, many=False)
        return Response(serializer.data)


class ByQuestionQuestionItemsList(ListAPIView):
    """Список вариантов ответа по идентификатору вопроса"""
    serializer_class = ViewQuestionItemSerializer

    def get(self, request, question_id, *args, **kwargs):
        self.queryset = QuestionItem.question_items.by_question(question_id)
        return super().get(request, *args, **kwargs)