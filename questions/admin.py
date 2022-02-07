from django.contrib import admin

from questions.models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "date")
    list_filter = ("date", 'category')
    search_fields = ("title", "text", 'category')
    ordering = ['profile', "date"]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "profile", "date")
    search_fields = ("title", "text", "category")
    ordering = ["question", "profile", "date"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
