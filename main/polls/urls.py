from django.urls import path
from polls.api.polls.views import \
    ListActivePoll, CreatePoll, \
    UpdatePoll, ViewPoll, \
    DestroyPoll, ListAllPoll
from polls.api.poll_sessions.views import \
    CreatePollSession, ViewPollSession, \
    FinishPollSession, ViewPollSessionDetail, \
    ViewPollSessionDetailByUserID
from polls.api.questions.views import \
    ListByPollQuestion, CreateQuestion, \
    DestroyQuestion, UpdateQuestion, ViewQuestion
from polls.api.question_items.views import \
    CreateQuestionItem, UpdateQuestionItem, \
    DestroyQuestionItem, ViewQuestionItem, \
    ByQuestionQuestionItemsList
from polls.api.answer.views import CreateAnswer

urlpatterns = [
    path('polls/active', ListActivePoll.as_view(), name='active-poll'),
    
    path('polls/all', ListAllPoll.as_view(), name='all-poll'),
    path('polls/create', CreatePoll.as_view(), name='create-poll'),
    path('polls/view/<int:pk>', ViewPoll.as_view(), name='view-poll'),
    path('polls/update/<int:pk>', UpdatePoll.as_view(), name='update-poll'),
    path('polls/destroy/<int:pk>', DestroyPoll.as_view(), name='destroy-poll'),

    path('poll_sessions/create', CreatePollSession.as_view(), name='create-poll-session'),
    path('poll_sessions/view/<int:pk>', ViewPollSession.as_view(), name='view-poll-session'),
    path('poll_sessions/detail/<int:pk>', ViewPollSessionDetail.as_view(), name='detail-poll-session'),
    path('poll_sessions/finish/<int:pk>', FinishPollSession.as_view(), name='finish-poll-session'),

    path('poll_sessions/completed_by_user_id/<int:user_id>', ViewPollSessionDetailByUserID.as_view(), name='completed-by-user-id'),



    path('questions/by_poll/<int:poll_id>', ListByPollQuestion.as_view(), name='by-poll-question'),
    path('questions/create', CreateQuestion.as_view(), name='create-question'),
    path('questions/view/<int:pk>', ViewQuestion.as_view(), name='view-question'),
    path('questions/update/<int:pk>', UpdateQuestion.as_view(), name='update-question'),
    path('questions/destroy/<int:pk>', DestroyQuestion.as_view(), name='destroy-question'),

    path('question_items/by_question/<int:question_id>', ByQuestionQuestionItemsList.as_view(), name='by-question-question-items'),
    path('question_items/create', CreateQuestionItem.as_view(), name='create-question-item'),
    path('question_items/view/<int:pk>', ViewQuestionItem.as_view(), name='view-question-item'),
    path('question_items/update/<int:pk>', UpdateQuestionItem.as_view(), name='update-question-item'),
    path('question_items/destroy/<int:pk>', DestroyQuestionItem.as_view(), name='destroy-question-item'),

    path('answer/create', CreateAnswer.as_view(), name='create-answer'),

]
