from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from survey.business_logic.QuestionRanking import QuestionRankingCalculator
from survey.models import Question, Answer, Vote


class TestQuestionRankingCalculator(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("sebastian", "fake@fake.com", "fakepassword")
        self.question = Question.objects.create(title="fake title", description="fake description", author=self.user)
        self.another_question = Question.objects.create(title="another fake title",
                                                        description="another fake description", author=self.user)
        self.calculator = QuestionRankingCalculator(queryset=Question.objects.filter(pk=self.question.pk))

    def test_get_question_with_ranking_created_today(self):
        self.assertEqual(self.calculator.get_question_with_ranking().first().ranking, self.calculator.TODAY_VALUE)

    def test_get_question_with_ranking_counts_answers(self):
        Answer.objects.create(question=self.question, author=self.user)
        Answer.objects.create(question=self.question, author=self.user)

        self.assertEqual(
            self.calculator.get_question_with_ranking().first().ranking,
            self.calculator.ANSWER_VALUE * 2 + self.calculator.TODAY_VALUE
        )

    def test_get_question_with_ranking_counts_likes_and_dislikes(self):
        another_user = User.objects.create_user("seba", "fake2@fake.com", "fakepassword")
        Vote.objects.create(question=self.question, author=self.user, like=True)
        Vote.objects.create(question=self.question, author=another_user, like=False)
        Vote.objects.create(question=self.another_question, author=self.user, like=True)
        Vote.objects.create(question=self.another_question, author=another_user, like=True)

        self.assertEqual(
            self.calculator.get_question_with_ranking().first().ranking,
            self.calculator.LIKE_VALUE + self.calculator.DISLIKE_VALUE + self.calculator.TODAY_VALUE
        )

    def test_get_question_with_ranking_without_answers_and_created_yesterday(self):
        self.question.created = date.today() - timedelta(days=1)
        self.question.save()

        self.assertEqual(self.calculator.get_question_with_ranking().first().ranking, 0)
