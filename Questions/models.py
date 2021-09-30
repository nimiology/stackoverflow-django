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

    title = models.CharField(max_length=2048)
    profile = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name=relatedName)
    category = models.ManyToManyField(Category, blank=True, related_name=relatedName)
    tech = models.ManyToManyField(Tech, blank=True, related_name=relatedName)
    text = models.TextField()
    pic = models.ImageField(upload_to=upload_image_Question, blank=True)
    slug = models.SlugField(blank=True)
    upVote = models.ManyToManyField(Wallet, blank=True, related_name='questionUpVote')
    downVote = models.ManyToManyField(Wallet, blank=True, related_name='questionDownVote')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.title}'


class Answer(models.Model):
    relatedName = 'answer'

    profile = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name=relatedName)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name=relatedName)
    text = models.TextField()
    pic = models.ImageField(upload_to=upload_image_Answer, blank=True)
    upVote = models.ManyToManyField(Wallet, blank=True, related_name='answerUpVote')
    downVote = models.ManyToManyField(Wallet, blank=True, related_name='answerDownVote')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.question.title}'


def Question_presave(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = slug_genrator(Question)


def Answer_presave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.question.profile,
                         notification='You have a new answer',
                         slug=instance.question.slug,
                         slugTo='q')
    Notif.save()


def AnswerUpVotePreSave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.answer.question.profile,
                         notification='Your Answer Voted Up',
                         slug=instance.answer.question.slug,
                         slugTo='q')
    Notif.save()


def AnswerDownVotePreSave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.question.profile,
                         notification='Your Answer Voted Down',
                         slug=instance.question.slug,
                         slugTo='q')
    Notif.save()


def QuestionDownVotePreSave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.answer.question.profile,
                         notification='Your Question Voted Down',
                         slug=instance.answer.question.slug,
                         slugTo='q')
    Notif.save()


def QuestionUpVotePreSave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.question.profile,
                         notification='Your Question Voted Up',
                         slug=instance.question.slug,
                         slugTo='q')
    Notif.save()


pre_save.connect(Question_presave, sender=Question)
pre_save.connect(Answer_presave, sender=Answer)
m2m_changed.connect(QuestionUpVotePreSave, sender=Question.upVote.through)
m2m_changed.connect(AnswerUpVotePreSave, sender=Answer.upVote.through)
m2m_changed.connect(AnswerDownVotePreSave, sender=Answer.downVote.through)
m2m_changed.connect(QuestionDownVotePreSave, sender=Question.downVote.through)
