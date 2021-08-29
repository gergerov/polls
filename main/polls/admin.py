from django.contrib import admin
from django.contrib.admin.decorators import register
from polls.models import *


@register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end', 'description', )
    list_filter = ('start', 'end', )
    search_fields = ('name', 'description', )


@register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('type', 'text', 'poll', 'pk', )
    search_fields = ('text', )


@register(QuestionItem)
class QuestionItemAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'pk', )
    search_fields = ('text', )


@register(PollSession)
class PollSessionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'user_id', 'finished',)
    search_fields = ('poll__name', )


@register(Answer)
class PollSessionAdmin(admin.ModelAdmin):
    list_display = ('poll_session', 'question', 'answer_item', 'answer_as_text', )
    search_fields = ('poll_session__poll__name', )

