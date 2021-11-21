from django.db import models
from django.db.models.signals import (
    pre_save,
    m2m_changed,
)
from users.models import (
    Employee,
    Company,
    Wallet,
    Notification,
)
from Posts.utils import (
    PictureAndVideoValidator,
    slug_genrator, upload_file,
)


class Hashtag(models.Model):
    title = models.CharField(max_length=1024, unique=True, primary_key=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    profile = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='post')
    slug = models.SlugField(blank=True, max_length=100)
    tag = models.ManyToManyField(Wallet, blank=True, related_name='tagInPost')
    description = models.TextField(blank=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True, related_name='post')
    like = models.ManyToManyField(Wallet, blank=True, related_name='likes')
    date = models.DateTimeField(auto_now_add=True)
    seo = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.profile}-{self.pk}'


class Comment(models.Model):
    profile = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    replyTo = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='commentsReply')
    text = models.TextField()
    tag = models.ManyToManyField(Wallet, blank=True, related_name='commentReply')
    like = models.ManyToManyField(Wallet, blank=True, related_name='commentLikes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.post}'


class Media(models.Model):
    thumbnail = models.FileField(upload_to=upload_file, blank=True, validators=[PictureAndVideoValidator])
    alt = models.CharField(max_length=300)
    media = models.FileField(upload_to=upload_file, blank=True, validators=[PictureAndVideoValidator])
    seo = models.JSONField(blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name='media')
    question = models.ForeignKey('Questions.Question', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='media')
    answer = models.ForeignKey('Questions.Answer', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='media')


def Post_presave(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = slug_genrator(Post)


def PostM2MChange(sender, instance, *args, **kwargs):
    if 'post_add' == kwargs['action']:
        if instance.tag.all():
            for profile in instance.tag.all():
                notification = Notification(profile=profile,
                                            text="You've been tagged on this post",
                                            slug=f'post/{instance.slug}')
                notification.save()


def Likes_presave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.profile,
                         text='Liked your message',
                         slug=f'post/{instance.slug}')
    Notif.save()


def Comments_presave(sender, instance, *args, **kwargs):
    Notif = Notification(profile=instance.post.profile,
                         text='You have a new comment',
                         slug=f'post/{instance.post.slug}')
    Notif.save()


def TagCommentPreSave(sender, instance, *args, **kwargs):
    if 'post_add' == kwargs['action']:
        if instance.tag.all():
            for person in instance.tag.all():
                Notif = Notification(profile=person,
                                     text='You have a new comment',
                                     slug=f'post/{instance.post.slug}')

                Notif.save()


pre_save.connect(Post_presave, sender=Post)
m2m_changed.connect(Likes_presave, sender=Post.like.through)
pre_save.connect(Comments_presave, sender=Comment)
m2m_changed.connect(PostM2MChange, sender=Post.tag.through)
m2m_changed.connect(TagCommentPreSave, sender=Comment.tag.through)
