from questions.views import *
from django.urls import path

urlpatterns = [
    path('question', QuestionAPI.as_view()),
    path('question/<slug>', QuestionAPI.as_view()),
    path('question/<slug>/upvote', QuestionUpVote.as_view()),
    path('question/<slug>/downvote', QuestionDownVote.as_view()),
    path('user/<slug>/question', AllUserQuestionsAPI.as_view()),
    path('questions', SearchQuestions.as_view()),

    path('question/<slug>/answer', AnswerAPI.as_view()),
    path('question/<slug>/answers', QuestionAnswers.as_view()),
    path('answer/<int:pk>', AnswerAPI.as_view()),
    path('answer/<int:pk>/upvote', AnswerUpVote.as_view()),
    path('answer/<int:pk>/downvote', AnswerDownVote.as_view()),

]