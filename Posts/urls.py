from Posts.views import *
from django.urls import path

urlpatterns = [
    path('post', PostAPI.as_view()),
    path('post/<slug>', PostAPI.as_view()),
    path('post/user/<slug>', UserPostsAPI.as_view()),
    path('seeposts', SeePosts.as_view()),

]