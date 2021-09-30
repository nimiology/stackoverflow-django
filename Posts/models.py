from django.db import models
from django.db.models.signals import pre_save, m2m_changed

from users.models import Employee, Company, Wallet, Notification
from .utils import *


class Hashtag(models.Model):
    title = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    profile = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='post')
    slug = models.SlugField(blank=True)
    pic = models.FileField(upload_to=upload_file_Post, blank=True, validators=[PictureAndVideoValidator])
    tag = models.ManyToManyField(Wallet, blank=True, related_name='tagInPost')
    description = models.TextField(blank=True)
    hashtag = models.ManyToManyField(Hashtag, related_name='post')
    like = models.ManyToManyField(Wallet, blank=True, related_name='likes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.pk}'


class Comment(models.Model):
    profile = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    replyTo = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='commentsReply')
    text = models.TextField()
    tag = models.ForeignKey(Wallet, blank=True, null=True, on_delete=models.CASCADE, related_name='commentReply')
    like = models.ManyToManyField(Wallet, blank=True, related_name='commentLikes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.post}'


def Post_presave(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = slug_genrator(Post)


def PostM2MChange(sender, instance, *args, **kwargs):
    if 'post_add' == kwargs['action']:
        if instance.tag.all():
            for profile in instance.tag.all():
                notification = Notification(profile=profile,
                                            text="You've been tagged on this post",
                                            slugTo='p',
                                            slug=f'post/{instance.slug}')
                notification.save()


def Likes_presave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.profile,
                         text='Liked your message',
                         slug=instance.slug,
                         slugTo=f'post/{instance.slug}')
    Notif.save()


def Comments_presave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.post.profile,
                         text='You have a new comment',
                         slug=f'post/{instance.post.slug}')
    Notif.save()
    if instance.tag:
        for person in instance.tag.all():
            Notif = Notification(profile=person,
                                 text='You have a new comment',
                                 slug=f'post/{instance.post.slug}')

            Notif.save()


pre_save.connect(Post_presave, sender=Post)
m2m_changed.connect(Likes_presave, sender=Post.like.through)
pre_save.connect(Comments_presave, sender=Comment)
m2m_changed.connect(PostM2MChange, sender=Post.tag.through)
