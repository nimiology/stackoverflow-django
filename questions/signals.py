from posts.utils import slug_generator
from users.models import Notification


def question_pre_save(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = slug_generator()


def questionDownVotePreSave(sender, instance, *args, **kwargs):
    notification = Notification(profile=instance.profile,
                                text='Your Question Voted Down',
                                slug=f'question/{instance.slug}')
    notification.save()


def questionUpVotePreSave(sender, instance, *args, **kwargs):
    notification = Notification(profile=instance.profile,
                                text='Your Question Voted Up',
                                slug=f'question/{instance.slug}')
    notification.save()


def answer_pre_save(sender, instance, *args, **kwargs):
    notification = Notification(profile=instance.question.profile,
                                text='You have a new answer',
                                slug=f'question/{instance.question.slug}')
    notification.save()


def answerUpVote_pre_save(sender, instance, *args, **kwargs):
    notification = Notification(profile=instance.question.profile,
                                text='Your Answer Voted Up',
                                slug=f'question/{instance.question.slug}')

    notification.save()


def answerDownVote_pre_save(sender, instance, *args, **kwargs):
    notification = Notification(profile=instance.question.profile,
                                text='Your Answer Voted Down',
                                slug=f'question/{instance.question.slug}')

    notification.save()