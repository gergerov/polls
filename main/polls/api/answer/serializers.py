from rest_framework import serializers

from polls.models import Answer
from polls.api.question_items.serializers import ViewQuestionItemSerializer


class ViewAnswerSerializer(serializers.ModelSerializer):
    answer_item = ViewQuestionItemSerializer(many=False)
    class Meta:
        model = Answer
        fields = ['answer_as_text', 'answer_item', 'question', 'poll_session', 'id', ]
        read_only_fields = ['answer_as_text', 'answer_item', 'question', 'poll_session', 'id', ]


class CreateAnswerSerializer(serializers.Serializer):
    poll_session_id = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True)
    question_item_id = serializers.IntegerField(required=False)
    text = serializers.CharField(required=False)
