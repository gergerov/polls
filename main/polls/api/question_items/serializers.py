from rest_framework import serializers
from polls.models import QuestionItem


class ViewQuestionItemSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра вариантов ответа на вопрос опроса"""
    class Meta:
        model = QuestionItem
        fields = ['text', 'pk', ]
        read_only_fields = ['text', 'pk', ]


class CreateQuestionItemSerializer(serializers.ModelSerializer):
    """Сериализатор для создания вариантов ответа на вопрос опроса"""
    class Meta:
        model = QuestionItem
        fields = ['text', 'question' ]


class UpdateQuestionItemSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления вариантов ответа на вопрос опроса"""
    class Meta:
        model = QuestionItem
        fields = ['text', ]


class DestroyQuestionItemSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления вариантов ответа на вопрос опроса"""
    class Meta:
        model = QuestionItem
        fields = ['pk', ]