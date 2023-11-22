from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Subquery, OuterRef
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView

from survey.business_logic.QuestionRanking import QuestionRankingCalculator
from survey.forms import AnswerForm
from survey.models import Question, Vote


class QuestionListView(ListView):
    model = Question

    def get_queryset(self):
        question_ranking_calculator = QuestionRankingCalculator(queryset=Question.objects.all())
        queryset = question_ranking_calculator.get_question_with_ranking().order_by("-ranking")
        queryset = queryset.annotate(
            current_user_answer=Subquery(
                queryset.filter(
                    answers__question_id=OuterRef("id"),
                    answers__author_id=self.request.user.id
                ).values("answers__value")[:1]
            )
        ).annotate(
            current_user_vote=Subquery(
                queryset.filter(
                    question_votes__question_id=OuterRef("id"),
                    question_votes__author_id=self.request.user.id
                ).values("question_votes__like")[:1]
            )
        )
        return queryset[:20]


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'description']
    success_url = reverse_lazy("survey:question-list")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(PermissionRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'
    permission_required = "change_question"


class AnswerFormView(LoginRequiredMixin, FormView):
    template_name = "survey/answer_form.html"
    form_class = AnswerForm
    success_url = reverse_lazy("survey:question-list")
    login_url = reverse_lazy("login")

    def get_initial(self):
        self.initial["value"] = self.request.GET.get("value", 0)
        return self.initial.copy()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question = get_object_or_404(Question, pk=self.kwargs.get('question_id'))
        form.save()
        return super().form_valid(form)


def vote_question(request, question_id, like):
    question = get_object_or_404(Question, pk=question_id)
    vote = Vote.objects.get_or_create(
        question=question,
        author=request.user
    )[0]
    vote.like = like
    vote.save()
    return redirect("survey:question-list")
