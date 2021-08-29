from django.db import models
from django.utils import timezone
from polls.managers import PollManager, QuestionManager, QuestionItemManager, PollSessionManager, AnswerManager


class Poll(models.Model):
    """Модель опроса. 'Атрибуты опроса: название, дата старта, дата окончания, описание.' """

    polls = PollManager()

    name = models.CharField(
        max_length=512
        , help_text="название опроса"
        , default="Опрос"
        , null=False
        , verbose_name="Название"
    )
    
    start = models.DateField(
        null=False
        , default=timezone.now
        , help_text="дата старта, после сохранения не редактируется"
        , verbose_name="Дата старта"
    )

    end = models.DateField(
        null=False
        , default=timezone.now
        , help_text="дата окончания опроса"
        , verbose_name="Дата окончания"        
    )

    description = models.TextField(
        max_length=2048
        , null=False
        , default="Описание опроса"
        , verbose_name="Описание"
    )

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    """
    Модель вопроса опроса. 
    'Атрибуты вопросов: 
    текст вопроса, 
    тип вопроса (
        ответ текстом
        , ответ с выбором одного варианта
        , ответ с выбором нескольких вариантов
    ) '
    """

    questions = QuestionManager()

    QUESTION_TYPES = [
        ('M', 'Multi'),
        ('S', 'Single'),
        ('T', 'Free text')
    ]

    text = models.TextField(
        max_length=1024
        , default="Вопрос"
        , null=False
        , verbose_name="Вопрос"
        , help_text="вопрос по опросу"
    )

    type = models.CharField(
        null=False
        , default='T'
        , choices=QUESTION_TYPES
        , verbose_name="Тип вопроса"
        , max_length=10
        
    )

    poll = models.ForeignKey(
        to=Poll
        , verbose_name="Опрос вопроса"
        , on_delete=models.DO_NOTHING
        , related_name="questions"
    )

    def __str__(self):
        return f'{self.text} TYPE: {self.type}'


class QuestionItem(models.Model):
    """Вариант ответа на вопрос"""
    
    text = models.TextField(
        max_length=1024
        , null=False
        , default="Ответ"
        , verbose_name="Вариант ответа"
    )

    question = models.ForeignKey(
        to=Question
        , verbose_name="Вариант ответа на вопрос"
        , on_delete=models.DO_NOTHING
        , related_name="question_items"
        , null=True
    )

    question_items = QuestionItemManager()
    objects = models.Manager()

    def __str__(self):
        return f'{self.text}'


class PollSession(models.Model):
    """Сессия опроса, ТЗ не предусмотрено, но напрашивается."""

    # sessions = PollSessionManager() 
    # менеджер сессий опросов, для управления случаями, когда
    # пользователь известен и уже проходил опрос и либо окончил его, либо не окончил его
    objects = models.Manager()
    poll_sessions = PollSessionManager()

    poll = models.ForeignKey(
        to=Poll
        , verbose_name="Опрос сессии"
        , on_delete=models.DO_NOTHING
    )
    
    user_id = models.IntegerField(
        verbose_name="Числовой идентификатор пользователя сессии опроса"
        , help_text="в ТЗ указано так, \
            будто пользователь может приходить из левой системы\
            , поэтому числовой ID, а не FK на base_auth_model"
        , null=True # если пустой, значит аноним
    )

    finished = models.BooleanField(
        verbose_name="Окончена ли сессия опроса"
        , default=False
        , null=False
        , db_index=True
    )

    session_id = models.IntegerField(
        verbose_name="Сессия для сессии опроса, если аноним"
        , help_text="Чтобы не хреначить кучу сессий опросов"
        , null=True # если пустой, значит не аноним
    )

    def __str__(self):
        user = ''
        if self.user_id:
            user = str(self.user_id)
        else:
            user = 'аноним'
        return f'{self.poll} User:{user} finished:{self.finished}'


class Answer(models.Model):
    """Ответ на вопрос сессии опроса"""

    answers = AnswerManager()
    objects = models.Manager()

    poll_session = models.ForeignKey(
        to=PollSession
        , on_delete=models.DO_NOTHING
        , verbose_name="Сессия опроса"
        , help_text="Сессия, в которой был дан ответ на вопрос"
        , null=False
        , related_name="answers"
    )

    question = models.ForeignKey(
        to=Question
        , verbose_name="Вопрос"
        , help_text="Вопрос, на который был дан ответ"
        , null=False
        , on_delete=models.DO_NOTHING
        , related_name="answers"
        
    )

    answer_item = models.ForeignKey(
        to=QuestionItem
        , verbose_name="Ответ"
        , on_delete=models.DO_NOTHING
        , help_text="Выбранный вариант ответа"
        , null=True
        , blank=True
    )

    answer_as_text = models.TextField(
        max_length=1024
        , verbose_name="Ответ как текст"
        , help_text="По ТЗ ответ может быть простым текстом"
        , null=True
        , blank=True
    )
