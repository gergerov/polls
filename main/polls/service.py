from polls.models import PollSession, Poll, Answer, Question, QuestionItem
from polls.api.answer.exceptions import *
from polls.api.poll_sessions.exceptions import *

from django.db import connection


def __create_session_object(poll_id, user_id=None):
    poll_session_object = PollSession()
    if user_id:
        poll_session_object = PollSession()
    poll_session_object.user_id = user_id
    poll_session_object.poll = Poll.polls.get(poll_id)
    poll_session_object.finished = False
    poll_session_object.save()
    return poll_session_object


def poll_session_get_or_create(poll_id, user_id=None):
    if user_id:
        if PollSession.objects.filter(poll__pk=poll_id, user_id=user_id).exists():
            return PollSession.objects.get(poll__pk=poll_id, user_id=user_id)
        else:
            return __create_session_object(poll_id, user_id)
    else:
        return __create_session_object(poll_id, user_id)


def create_answer(poll_session_id, question_id, question_item_id=None, text=None):
    poll_session_object = PollSession.poll_sessions.get(poll_session_id)
    question_object = Question.questions.get(question_id)
    # если сессия опроса уже завершена, ответы не принимаются
    if poll_session_object.finished == True:
        raise AnswerOnFinishedPollSession
    # дают ли нам ответ на вопрос, который есть в опросе
    if poll_session_object.poll != question_object.poll:
        raise PollDoesNotHaveThisQuestion
    
    if question_object.type == 'T':
        return __create_answer_on_text(poll_session_object, question_object, text)
    if question_object.type == 'M':
        return __create_answer_on_multi(poll_session_object, question_object, question_item_id)
    if question_object.type == 'S':
        return __create_answer_on_single(poll_session_object, question_object, question_item_id)


def __create_answer_on_single(poll_session_object, question_object, question_item_id=None):
    if question_item_id is None:
        raise AnswerByThisQuestionMustHaveItem

    if Answer.objects.filter(poll_session__pk=poll_session_object.pk, question__pk=question_object.pk).exists():
        raise AnswerOnThisQuestionAlreadyExists

    question_item_object = QuestionItem.question_items.get(question_item_id)
    __question_item_exists_in_question(question_object, question_item_object)

    answer = Answer.objects.create(poll_session=poll_session_object, question=question_object, answer_item=question_item_object)
    return answer


def __create_answer_on_multi(poll_session_object, question_object, question_item_id=None):
    if question_item_id is None:
        raise AnswerByThisQuestionMustHaveItem
    
    if Answer.objects.filter(poll_session__pk=poll_session_object.pk, question__pk=question_object.pk, answer_item__pk=question_item_id).exists():
        raise AnswerItemOnThisMultiQuestionAlreadyExists

    question_item_object = QuestionItem.question_items.get(question_item_id)
    __question_item_exists_in_question(question_object, question_item_object)
    
    answer = Answer.objects.create(poll_session=poll_session_object, question=question_object, answer_item=question_item_object)
    return answer


def __create_answer_on_text(poll_session_object, question_object, text=None):
    if question_object.type == 'T' and text is None:
        raise AnswerByThisQuestionMustHaveText

    if Answer.objects.filter(poll_session__pk=poll_session_object.pk, question__pk=question_object.pk).exists():
        raise AnswerOnThisQuestionAlreadyExists

    answer = Answer.objects.create(poll_session=poll_session_object, question=question_object, answer_as_text=text)
    return answer
    

def __question_item_exists_in_question(question_object, question_item_object):
    """Проверка, есть ли у вопроса такой вариант ответа"""
    poll_questions = QuestionItem.question_items.by_question(question_object.pk)
    if question_item_object not in poll_questions:
        raise AnswerQuestionItemNotInThisQuestionItems


def finish_poll_session(poll_session_id):
    poll_session_object = PollSession.poll_sessions.get(poll_session_id)
    poll_object = Poll.polls.get(poll_session_object.poll.pk)
    answered_questions = Answer.answers.by_poll_session(poll_session_id).values('question').distinct().count()
    all_questions = poll_object.questions.count()

    if answered_questions != all_questions:
        raise NotAllQuestionsAnswered
    else:
        PollSession.poll_sessions.finish(poll_session_id)


def poll_session_info(poll_session_id):
    SQL = """
        select 
            ps.id as poll_session_id, 
            ps.user_id as user_id, 
            ps.poll_id as poll_id, 
            ps.finished as finished,
            count(distinct qanswered.id) as answered_questions,
            count(distinct all_questions.id) as all_questions

        from 
            polls_pollsession ps
            left join polls_answer a on ps.id = a.poll_session_id
                left join polls_question qanswered on a.question_id = qanswered.id
            
            inner join polls_poll p on ps.poll_id = p.id
                inner join polls_question all_questions on all_questions.poll_id = p.id
        where
            ps.id = %s
	    """
    with connection.cursor() as cursor:
        cursor.execute(SQL, [poll_session_id])
        return __dictfetchall(cursor=cursor)


def poll_session_detail(poll_session_id):
    SQL = """
    select 

        all_questions.text 	question_text,
        all_questions.type 	question_type,
        a.answer_as_text	answer_text,
        qi.text				question_item_text,
        
        all_questions.id    question_id,
        a.id				answer_id,
        qi.id				question_item_id,
        ps.poll_id          poll_id
	

    from 
        polls_pollsession ps

        inner join polls_poll p on ps.poll_id = p.id
            inner join polls_question all_questions on all_questions.poll_id = p.id
            
            left join polls_answer a on ps.id = a.poll_session_id and a.question_id = all_questions.id
                left join polls_questionitem qi on a.answer_item_id = qi.id
	where 
        ps.id=%s
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL, [poll_session_id])
        return __dictfetchall(cursor=cursor)


def poll_session_unanswered_questions(poll_session_id):
    SQL = """
    select 
        all_questions.text 	question_text,
        all_questions.type 	question_type,	
        all_questions.id    question_id
    from 
        polls_pollsession ps
        inner join polls_poll p on ps.poll_id = p.id
            inner join polls_question all_questions on all_questions.poll_id = p.id
            
            left join polls_answer a on ps.id = a.poll_session_id and a.question_id = all_questions.id
                left join polls_questionitem qi on a.answer_item_id = qi.id
    where 
        ps.id=%s
        and a.id is null
    """
    with connection.cursor() as cursor:
        cursor.execute(SQL, [poll_session_id])
        return __dictfetchall(cursor=cursor)


def __dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]