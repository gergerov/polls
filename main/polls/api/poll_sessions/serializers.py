from django.db.models import fields
from rest_framework import serializers
from polls.models import PollSession


class CreatePollSessionSerializer(serializers.Serializer):
    """Сериализатор для создания сессии опроса"""
    poll_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)


class ViewPollSessionSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра сессии опроса"""
    # poll = ViewPollSerializer(many=False)
    # answers = ViewAnswerSerializer(many=True)

    class Meta:
        model = PollSession
        fields = ['poll', 'user_id', 'finished', ]
        read_only_fields = ['finished', 'poll', 'user_id', ]
        

class ViewPollSessionDetailSerializer(serializers.Serializer):
    """Сериализатор для просмотра деталей сессии опроса"""
    question_text = serializers.CharField(required=True)
    question_type = serializers.CharField(required=True)
    answer_id = serializers.IntegerField(required=True)
    poll_id = serializers.IntegerField(required=True)
    answer_text = serializers.CharField(required=False, allow_null=True)
    question_item_text = serializers.CharField(required=False, allow_null=True)
    question_id = serializers.IntegerField(required=False, allow_null=True)
    question_item_id = serializers.IntegerField(required=False, allow_null=True)


class ViewPollSessionInfoSerializer(serializers.Serializer):
    """Сериализатор информации по сессии опроса"""
    details = ViewPollSessionDetailSerializer(many=True)
    poll_session_id = serializers.IntegerField(required=True)
    poll_id = serializers.IntegerField(required=True)
    finished = serializers.BooleanField(required=True)
    answered_questions = serializers.IntegerField(required=True)
    all_questions = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)


class ViewPollSessionInfoByUserIdSerrializer(serializers.Serializer):
    sessions = ViewPollSessionInfoSerializer(many=True)

