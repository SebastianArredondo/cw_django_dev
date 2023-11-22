from django.forms import ModelForm
from survey.models import Answer


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["value", "comment"]
