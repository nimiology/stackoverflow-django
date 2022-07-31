from posts.views import *
from django.urls import path

app_name = 'post'

urlpatterns = [
    path('posts/<str:slug>/', PostAPI.as_view(), name='post'),
    path('posts/', PostsListAPI.as_view(), name='posts_list'),
    path('seeposts/', SeePosts.as_view(), name='see_post'),

    path('posts/<slug>/like/', PostLike.as_view(), name='post_like'),

    path('comments/', CommentsListAPI.as_view(), name='comments_list'),
    path('comments/<int:pk>/', CommentAPI.as_view(), name='comment'),
    path('comments/<int:pk>/like/', CommentLike.as_view(), name='comment_like'),

    path('hashtags/<title>/', HashtagAPI.as_view(), name='hashtag'),
    path('hashtags/all/', HashtagsListAPI.as_view(), name='hashtags_list'),

]
