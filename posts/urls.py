from posts.views import *
from django.urls import path

app_name = 'post'

urlpatterns = [
    path('post/<str:slug>/', PostAPI.as_view(), name='post'),
    path('posts/', PostsListAPI.as_view(), name='posts_list'),
    path('seeposts/', SeePosts.as_view(), name='see_post'),

    path('post/<slug>/like/', Like.as_view(), name='post_like'),

    path('comment/', CommentsListAPI.as_view(), name='comments_list'),
    path('comment/<int:pk>/', CommentAPI.as_view(), name='comment'),
    path('comment/<int:pk>/like/', CommentLike.as_view(), name='comment_like'),

    path('hashtag/<title>/', HashtagAPI.as_view(), name='hashtag'),
    path('hashtag/all/', HashtagsListAPI.as_view(), name='hashtags_list'),

]
