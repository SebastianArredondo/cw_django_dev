from django.urls import path

from survey.views import (QuestionListView,
                          QuestionCreateView,
                          QuestionUpdateView,
                          AnswerFormView,
                          vote_question)

urlpatterns = [
    path('', QuestionListView.as_view(), name='question-list'),
    path('question/add/', QuestionCreateView.as_view(), name='question-create'),
    path('question/edit/<int:pk>', QuestionUpdateView.as_view(), name='question-edit'),
    path('question/<int:question_id>/answer', AnswerFormView.as_view(), name='question-answer'),
    path('question/<int:question_id>/like/<int:like>', vote_question, name='question-like'),


]