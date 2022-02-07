from questions.views import *
from django.urls import path

app_name = 'question'

urlpatterns = [
    path('question', QuestionAPI.as_view(), name='create_question'),
    path('question/<slug>', QuestionAPI.as_view(), name='question'),
    path('question/<slug>/upvote', QuestionUpVote.as_view(), name='upvote_question'),
    path('question/<slug>/downvote', QuestionDownVote.as_view(), name='downvote_question'),
    path('user/<slug>/question', AllUserQuestionsAPI.as_view(), name='user_questions'),
    path('questions', SearchQuestions.as_view(), name='questions'),

    path('question/<slug>/answer', AnswerAPI.as_view(), name='create_answer'),
    path('question/<slug>/answers', QuestionAnswers.as_view(), name='question_answers'),
    path('answer/<int:pk>', AnswerAPI.as_view(), name='answer'),
    path('answer/<int:pk>/upvote', AnswerUpVote.as_view(), name='upvote_answer'),
    path('answer/<int:pk>/downvote', AnswerDownVote.as_view(), name='downvote_answer'),

]