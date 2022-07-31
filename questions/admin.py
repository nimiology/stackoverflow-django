from django.contrib import admin

from questions.models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "date")
    list_filter = ("date", 'categories')
    search_fields = ("title", "text", 'categories')
    ordering = ['profile', "date"]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "profile", "date")
    search_fields = ("title", "text")
    ordering = ["question", "profile", "date"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
