from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Question(models.Model):
    created = models.DateField('Creada', auto_now_add=True)
    author = models.ForeignKey(get_user_model(), related_name="questions", verbose_name='Pregunta',
                               on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')

    # TODO: Quisieramos tener un ranking de la pregunta, con likes y dislikes dados por los usuarios.

    def get_absolute_url(self):
        return reverse('survey:question-edit', args=[self.pk])


class Answer(models.Model):
    ANSWERS_VALUES = ((0, 'Sin Responder'),
                      (1, 'Muy Bajo'),
                      (2, 'Bajo'),
                      (3, 'Regular'),
                      (4, 'Alto'),
                      (5, 'Muy Alto'),)

    question = models.ForeignKey(Question, related_name="answers", verbose_name='Pregunta', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), related_name="answers", verbose_name='Autor', on_delete=models.CASCADE)
    value = models.PositiveIntegerField("Respuesta", default=0, choices=ANSWERS_VALUES)
    comment = models.TextField("Comentario", default="", blank=True)


class Vote(models.Model):
    question = models.ForeignKey(Question, related_name="question_votes", verbose_name='Pregunta',
                                 on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), related_name="author_votes", verbose_name='Autor',
                               on_delete=models.CASCADE)
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ["question", "author"]
