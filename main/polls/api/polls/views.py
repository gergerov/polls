from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from polls.api.polls.serializers import \
    ListPollSerializer, ListPollDetailSerializer, \
    UpdatePollSerializer, CreatePollSerializer, \
    ViewPollSerializer, DestroyPollSerializer

from polls.models import Poll


class PollPagination(PageNumberPagination):
    """Пагинатор для листа опросов"""
    page_size = 15
    max_page_size = 150


class ListActivePoll(ListAPIView):
    """
        Список активных опросов. 
        Отображает все опросы дата начала которых уже наступила,
        а дата окончания - ещё нет.
        Без параметров
    """
    serializer_class = ListPollSerializer
    queryset = Poll.polls.active_polls().order_by('start', 'end')
    pagination_class = PollPagination


class ListAllPoll(ListAPIView):
    """Список всех опросов. Для того, чтобы было что в фронтовой админке смотреть."""
    serializer_class = ListPollDetailSerializer
    queryset = Poll.polls.all().order_by('start', 'end')
    pagination_class = PollPagination


class CreatePoll(CreateAPIView):
    """
        Создание опроса.
        Параметры: 'name', 'start', 'end', 'description'
    """
    serializer_class = CreatePollSerializer
    permission_classes = [IsAdminUser]


class UpdatePoll(UpdateAPIView):
    """Обновление опроса по pk в строке get запроса"""
    serializer_class = UpdatePollSerializer
    queryset = Poll.polls.all()
    permission_classes = [IsAdminUser]


class DestroyPoll(DestroyAPIView):
    """Удаление опроса  по pk в строке get запроса"""
    serializer_class = DestroyPollSerializer
    queryset = Poll.polls.all()
    permission_classes = [IsAdminUser]


class ViewPoll(APIView):
    """Просмотр опроса (детальный с вопросами) по pk в строке get запроса"""
    queryset = Poll.polls.all().select_related()

    def get(self, request, pk):
        obj = Poll.polls.get(pk)
        serializer = ViewPollSerializer(obj, many=False)
        return Response(serializer.data)

