from posts.utils import slug_generator
from users.models import Notification


def post_pre_save(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = slug_generator()


def post_M2M_changed(sender, instance, *args, **kwargs):
    if 'post_add' == kwargs['action']:
        if instance.tag.all():
            for profile in instance.tag.all():
                notification = Notification(profile=profile,
                                            text="You've been tagged on this post",
                                            slug=f'post/{instance.slug}')
                notification.save()


def likes_pre_save(sender, instance, *args, **kwargs):
    notification = Notification(profile=instance.profile,
                                text='Liked your message',
                                slug=f'post/{instance.slug}')
    notification.save()


def comments_pre_save(sender, instance, *args, **kwargs):
    notification = Notification(profile=instance.post.profile,
                                text='You have a new comment',
                                slug=f'post/{instance.post.slug}')
    notification.save()


def tag_comment_pre_save(sender, instance, *args, **kwargs):
    if 'post_add' == kwargs['action']:
        if instance.tag.all():
            for person in instance.tag.all():
                notification = Notification(profile=person,
                                            text='You have a new comment',
                                            slug=f'post/{instance.post.slug}')

                notification.save()