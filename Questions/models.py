from django.db import models
from django.db.models.signals import pre_save, m2m_changed

from users.models import (Tech,
                          Wallet,
                          Category,
                          Notification,
                          slug_genrator,
                          upload_image_Question,
                          upload_image_Answer,
                          )


# Create your models here.
class Question(models.Model):
    relatedName = 'question'

    profile = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name=relatedName)
    title = models.CharField(max_length=2048)
    category = models.ManyToManyField(Category, blank=True, related_name=relatedName)
    tech = models.ManyToManyField(Tech, blank=True, related_name=relatedName)
    text = models.TextField()
    slug = models.SlugField(blank=True,max_length=100)
    upVote = models.ManyToManyField(Wallet, blank=True, related_name='questionUpVote')
    downVote = models.ManyToManyField(Wallet, blank=True, related_name='questionDownVote')
    date = models.DateTimeField(auto_now_add=True)
    seo = models.JSONField(blank=True,null=True)

    def __str__(self):
        return f'{self.profile}-{self.title}'


class Answer(models.Model):
    relatedName = 'answer'

    profile = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name=relatedName)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name=relatedName)
    text = models.TextField()
    upVote = models.ManyToManyField(Wallet, blank=True, related_name='answerUpVote')
    downVote = models.ManyToManyField(Wallet, blank=True, related_name='answerDownVote')
    date = models.DateTimeField(auto_now_add=True)
    seo = models.JSONField(blank=True,null=True)

    def __str__(self):
        return f'{self.profile}-{self.question.title}'


def QuestionPreSave(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = slug_genrator(Question)


def AnswerPreSave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.question.profile,
                         text='You have a new answer',
                         slug=f'question/{instance.question.slug}')
    Notif.save()


def AnswerUpVotePreSave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.question.profile,
                         text='Your Answer Voted Up',
                         slug=f'question/{instance.question.slug}')

    Notif.save()


def AnswerDownVotePreSave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.question.profile,
                         text='Your Answer Voted Down',
                         slug=f'question/{instance.question.slug}')

    Notif.save()


def QuestionDownVotePreSave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.profile,
                         text='Your Question Voted Down',
                         slug=f'question/{instance.slug}')
    Notif.save()


def QuestionUpVotePreSave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.profile,
                         text='Your Question Voted Up',
                         slug=f'question/{instance.slug}')
    Notif.save()


pre_save.connect(QuestionPreSave, sender=Question)
pre_save.connect(AnswerPreSave, sender=Answer)
m2m_changed.connect(QuestionUpVotePreSave, sender=Question.upVote.through)
m2m_changed.connect(AnswerUpVotePreSave, sender=Answer.upVote.through)
m2m_changed.connect(AnswerDownVotePreSave, sender=Answer.downVote.through)
m2m_changed.connect(QuestionDownVotePreSave, sender=Question.downVote.through)
