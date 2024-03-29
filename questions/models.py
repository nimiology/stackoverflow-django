from django.db import models
from django.db.models.signals import pre_save, m2m_changed

from config import settings
from posts.utils import PictureAndVideoValidator, upload_file
from questions.signals import question_pre_save, questionUpVotePreSave, questionDownVotePreSave, answer_pre_save, \
    answerUpVote_pre_save, answerDownVote_pre_save
from users.models import Tech, Category

Users = settings.AUTH_USER_MODEL


class Question(models.Model):
    relatedName = 'question'

    profile = models.ForeignKey(Users, on_delete=models.CASCADE, related_name=relatedName)
    title = models.CharField(max_length=2048)
    categories = models.ManyToManyField(Category, blank=True, related_name=relatedName)
    techs = models.ManyToManyField(Tech, blank=True, related_name=relatedName)
    text = models.TextField()
    slug = models.SlugField(blank=True, max_length=100)
    media = models.FileField(upload_to=upload_file, blank=True,
                             null=True, validators=[PictureAndVideoValidator])
    upVote = models.ManyToManyField(Users, blank=True, related_name='questionUpVote')
    downVote = models.ManyToManyField(Users, blank=True, related_name='questionDownVote')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.title}'


class Answer(models.Model):
    relatedName = 'answer'

    profile = models.ForeignKey(Users, on_delete=models.CASCADE, related_name=relatedName)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name=relatedName)
    text = models.TextField()
    media = models.FileField(upload_to=upload_file, blank=True,
                             null=True, validators=[PictureAndVideoValidator])
    upVote = models.ManyToManyField(Users, blank=True, related_name='answerUpVote')
    downVote = models.ManyToManyField(Users, blank=True, related_name='answerDownVote')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.question.title}'


pre_save.connect(question_pre_save, sender=Question)
m2m_changed.connect(questionUpVotePreSave, sender=Question.upVote.through)
m2m_changed.connect(questionDownVotePreSave, sender=Question.downVote.through)
pre_save.connect(answer_pre_save, sender=Answer)
m2m_changed.connect(answerUpVote_pre_save, sender=Answer.upVote.through)
m2m_changed.connect(answerDownVote_pre_save, sender=Answer.downVote.through)
