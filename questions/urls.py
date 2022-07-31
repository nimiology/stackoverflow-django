from questions.views import *
from django.urls import path

app_name = 'question'

urlpatterns = [
    path('questions/', QuestionsListAPI.as_view(), name='questions_list'),
    path('questions/<slug>/', QuestionAPI.as_view(), name='question'),
    path('questions/<slug>/upvote/', QuestionUpVote.as_view(), name='upvote_question'),
    path('questions/<slug>/downvote/', QuestionDownVote.as_view(), name='downvote_question'),

    path('answers/', AnswersListAPI.as_view(), name='answers_list'),
    path('answers/<int:pk>/', AnswerAPI.as_view(), name='answer'),
    path('answers/<int:pk>/upvote/', AnswerUpVote.as_view(), name='upvote_answer'),
    path('answers/<int:pk>/downvote/', AnswerDownVote.as_view(), name='downvote_answer'),

]