from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from polls.api.questions.serializers import \
    ViewQuestionSerializer, CreateQuestionSerializer, \
    UpdateQuestionSerializer, DestroyQuestionSerializer
from polls.models import Question


class QuestionPagination(PageNumberPagination):
    """Пагинатор для листа вопросов опроса"""
    page_size = 1
    max_page_size = 2


class ListByPollQuestion(ListAPIView):
    """Список вопросов опроса по id опроса"""
    serializer_class = ViewQuestionSerializer
    pagination_class = QuestionPagination

    def get(self, request, poll_id, *args, **kwargs):
        self.queryset = Question.questions.by_poll(poll_id)
        return super().get(request, *args, **kwargs)
    

class CreateQuestion(CreateAPIView):
    """Создание вопроса: 'text', 'type', 'poll'"""
    permission_classes = [IsAdminUser]
    serializer_class = CreateQuestionSerializer


class UpdateQuestion(UpdateAPIView):
    """Обновление вопроса по идентификатору из строки get запроса"""
    permission_classes = [IsAdminUser]
    serializer_class = UpdateQuestionSerializer
    queryset = Question.questions.all()


class DestroyQuestion(DestroyAPIView):
    """Удаление вопроса"""
    permission_classes = [IsAdminUser]
    serializer_class = DestroyQuestionSerializer
    queryset = Question.questions.all()


class ViewQuestion(APIView):
    """Просмотр вопроса по идентификатору из строки get запроса"""
    queryset = Question.questions.all().select_related()

    def get(self, request, pk):
        obj = Question.questions.get(pk)
        serializer = ViewQuestionSerializer(obj, many=False)
        return Response(serializer.data)