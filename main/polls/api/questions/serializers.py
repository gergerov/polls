from rest_framework import serializers
from polls.models import Question
from polls.api.question_items.serializers import ViewQuestionItemSerializer



class ViewQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра вопроса опроса"""
    question_items = ViewQuestionItemSerializer(many=True) 
    class Meta:
        model = Question
        fields = ['pk', 'text', 'type', 'question_items', ]
        read_only_fields = ['pk', 'text', 'type', 'question_items', ]


class CreateQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для создания вопроса опроса"""
    class Meta:
        model = Question
        fields = ['text', 'type', 'poll', ]


class UpdateQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления вопроса опроса"""
    class Meta:
        model = Question
        fields = ['text', ]


class DestroyQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для удаления вопроса опроса"""
    class Meta:
        model = Question
        fields = ['pk', ]
