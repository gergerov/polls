from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404


class PollManager(models.Manager):
    
    def active_polls(self):
        return self.get_queryset().filter(start__lte=timezone.now(), end__gte=timezone.now())

    def all(self):
        return self.get_queryset()

    def get(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)


class PollSessionManager(models.Manager):
    
    def get(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)

    def finish(self, pk):
        obj = self.get(pk)
        obj.finished = True
        obj.save()
        return obj

    def completed_by_user_id(self, user_id):
        return self.get_queryset().filter(user_id=user_id, finished=True)


class QuestionManager(models.Manager):
    
    def by_poll(self, poll_id):
        return self.get_queryset().filter(poll__pk=poll_id)

    def all(self):
        return self.get_queryset()

    def get(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)


class QuestionItemManager(models.Manager):
    
    def all(self):
        return self.get_queryset()

    def get(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)

    def by_question(self, question_id):
        return self.get_queryset().filter(question__pk=question_id)


class AnswerManager(models.Manager):
    
    def all(self):
        return self.get_queryset()

    def get(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)

    def by_poll_session(self, poll_session_id):
        return self.get_queryset().filter(poll_session__pk=poll_session_id)
