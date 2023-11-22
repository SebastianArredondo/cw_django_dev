from datetime import date
from django.db.models import Case, Value, When, Count, Q
from survey.models import Question


class QuestionRankingCalculator:
    ANSWER_VALUE = 10
    TODAY_VALUE = 10
    LIKE_VALUE = 5
    DISLIKE_VALUE = -3

    def __init__(self, queryset: Question):
        self.queryset = queryset

    def get_question_with_ranking(self) -> Question:
        queryset = self.queryset.annotate(ranking=(
            Case(
                When(created=date.today(), then=Value(self.TODAY_VALUE)),
                default=Value(0),
            ) +
            Count("answers") * self.ANSWER_VALUE +
            Count("question_votes", filter=Q(question_votes__like=True)) * self.LIKE_VALUE) +
            Count("question_votes", filter=Q(question_votes__like=False)) * self.DISLIKE_VALUE
        )
        return queryset

