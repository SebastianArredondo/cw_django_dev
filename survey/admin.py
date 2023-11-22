from django.contrib import admin
from survey.models import Answer, Vote


class AnswerAdmin(admin.ModelAdmin):
    pass


class VoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Vote, VoteAdmin)
