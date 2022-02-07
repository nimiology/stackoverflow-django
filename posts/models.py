from django.db import models
from django.db.models.signals import pre_save, m2m_changed

from config import settings
from posts.signals import post_pre_save, likes_pre_save, comments_pre_save,\
    tag_comment_pre_save, post_M2M_changed
from users.models import Employee, Company
from posts.utils import PictureAndVideoValidator, upload_file

Users = settings.AUTH_USER_MODEL


class Hashtag(models.Model):
    title = models.CharField(max_length=1024, unique=True, primary_key=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    profile = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='post')
    slug = models.SlugField(blank=True, max_length=100)
    tag = models.ManyToManyField(Users, blank=True, related_name='tagInPost')
    description = models.TextField(blank=True, null=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True, related_name='post')
    like = models.ManyToManyField(Users, blank=True, related_name='likes')
    media = models.FileField(upload_to=upload_file, editable=False, blank=True,
                             null=True, validators=[PictureAndVideoValidator])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.pk}'


class Comment(models.Model):
    profile = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    replyTo = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='commentsReply')
    text = models.TextField()
    tag = models.ManyToManyField(Users, blank=True, related_name='commentReply')
    like = models.ManyToManyField(Users, blank=True, related_name='commentLikes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.post}'


pre_save.connect(post_pre_save, sender=Post)
m2m_changed.connect(likes_pre_save, sender=Post.like.through)
pre_save.connect(comments_pre_save, sender=Comment)
m2m_changed.connect(post_M2M_changed, sender=Post.tag.through)
m2m_changed.connect(tag_comment_pre_save, sender=Comment.tag.through)
