from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from polls.api.poll_sessions.serializers import \
    CreatePollSessionSerializer, ViewPollSessionSerializer, \
    ViewPollSessionInfoSerializer, ViewPollSessionInfoByUserIdSerrializer
from polls.service import \
    poll_session_get_or_create, finish_poll_session, \
    poll_session_info, poll_session_detail
from polls.models import PollSession


class CreatePollSession(CreateAPIView):
    """
        Создание сессии опроса или получение существующей
        (ТЗ умалчивает, но не будет же один и тот же юзер 100 раз опрос проходить, смысл ?)
        обязательно идентификатор опроса (poll_id) и необязательно идентификатор пользователя (user_id).
    """
    serializer_class = CreatePollSessionSerializer

    def post(self, request, *args, **kwargs):
        create_serializer = CreatePollSessionSerializer(data=request.POST)
        if create_serializer.is_valid():
            poll_session_object = poll_session_get_or_create(**create_serializer.data)
            return Response(data={"poll_session_id": poll_session_object.pk}, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST, data=create_serializer.errors)
    

class ViewPollSession(APIView):
    """Общая информация о сессии опроса по идентификатору в строке get запроса"""
    serializer_class = ViewPollSessionSerializer

    def get(self, request, pk, *args, **kwargs):
        obj = PollSession.poll_sessions.get(pk)
        serializer = ViewPollSessionSerializer(obj, many=False)
        return Response(serializer.data)


class ViewPollSessionDetail(APIView):
    """Детальная информация о сессии опроса по идентификатору в строке get запроса"""
    serializer_class = ViewPollSessionInfoSerializer

    def get(self, request, pk, *args, **kwargs):
        PollSession.poll_sessions.get(pk) # проверка на существование сессии
        poll_session_info_dict = poll_session_info(pk)[0]
        poll_session_info_dict['details'] = poll_session_detail(pk)
        serializer = ViewPollSessionInfoSerializer(data=poll_session_info_dict)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewPollSessionDetailByUserID(ListAPIView):
    """
        Показывает завершенные сессии опросов по идентификатору пользователя.
        - получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя.
        Показывает не только 'что выбрано', но и что введено, т.к. по ТЗ может быть текстовый ответ на вопрос.
    """
    serializer_class = ViewPollSessionInfoByUserIdSerrializer

    def get(self, request, user_id, *args, **kwargs):
        poll_sessions = PollSession.poll_sessions.completed_by_user_id(user_id).values('pk')
        poll_session_infos = []

        for pk in poll_sessions:
            id = pk['pk']
            poll_session_info_dict = poll_session_info(id)[0]
            poll_session_info_dict['details'] = poll_session_detail(id)
            poll_session_infos.append(poll_session_info_dict)
        
        serializer = ViewPollSessionInfoByUserIdSerrializer(data={"sessions": poll_session_infos})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK, data=serializer.errors)


class FinishPollSession(APIView):
    """
        Заканчивает сессию опроса по идентификатору в строке get запроса
        , сервис проводит проверку на 'отвеченность' всех вопросов опроса
    """
    def post(self, request, pk, *args, **kwargs):
        finish_poll_session(pk)
        return Response(status=status.HTTP_200_OK)