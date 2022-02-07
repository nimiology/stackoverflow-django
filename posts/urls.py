from posts.views import *
from django.urls import path

app_name = 'post'

urlpatterns = [
    path('post', PostAPI.as_view(), name='create_post'),
    path('post/<slug>', PostAPI.as_view(), name='post'),
    path('post/user/<slug>', UserPostsAPI.as_view(), name='user_post'),
    path('seeposts', SeePosts.as_view(), name='see_post'),

    path('post/<slug>/like', Like.as_view(), name='post_like'),

    path('post/<slug>/comment', CommentAPI.as_view(), name='create_comment'),
    path('comment/<int:pk>', CommentAPI.as_view(), name='comment'),
    path('comment/<int:pk>/like', CommentLike.as_view(), name='comment_like'),
    path('post/<slug>/comments', PostCommentsAPI.as_view(), name='post_comments'),

    path('hashtag', HashtagAPI.as_view(), name='create_hashtag'),
    path('hashtag/<pk>', HashtagAPI.as_view(), name='hashtag'),
    path('hashtag/<id>/posts', HashtagPostAPI.as_view(), name='hashtag_posts'),
    path('hashtags', AllHashtagsAPI.as_view(), name='hashtags'),
]
