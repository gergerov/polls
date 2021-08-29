from rest_framework import serializers
from polls.models import Poll
from polls.api.questions.serializers import ViewQuestionSerializer


class ListPollSerializer(serializers.ModelSerializer):
    """Сериализатор для списка активных опросов"""
    class Meta:
        model = Poll
        fields = [ 'pk', 'name', 'start', 'end', 'description', ]
        read_only_fields = [ 'pk', 'name', 'start', 'end', 'description', ]


class ListPollDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для списка всех опросов под представление all"""
    questions = ViewQuestionSerializer(many=True)
    class Meta:
        model = Poll
        fields = [ 'pk', 'name', 'start', 'end', 'description', 'questions']
        read_only_fields = ['pk', 'name', 'start', 'end', 'description', 'questions', ]


class CreatePollSerializer(serializers.ModelSerializer):
    """Сериализатор для создания опроса"""
    class Meta:
        model = Poll
        fields = ['name', 'start', 'end', 'description', ]


class UpdatePollSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления опроса, по ТЗ дату старта обновлять после создания нельзя"""
    class Meta:
        model = Poll
        fields = ['name', 'start', 'end', 'description', ]
        read_only_fields = ['start', ]


class ViewPollSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра опроса с вопросами"""
    questions = ViewQuestionSerializer(many=True)
    class Meta:
        model = Poll
        fields = ['pk', 'name', 'start', 'end', 'description', 'questions', ]
        read_only_fields = ['pk', 'name', 'start', 'end', 'description', 'questions', ]


class DestroyPollSerializer(serializers.ModelSerializer):
    """Сериализатор для удаления опроса"""
    class Meta:
        model = Poll
        fields = ['pk',]
    
