from django.contrib import admin
from Posts.models import Post, Comment, Hashtag


class PostAdmin(admin.ModelAdmin):
    list_display = ("profile", "slug", 'date')
    ordering = ["profile", "id", 'date']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("profile", "post", 'date')
    ordering = ["profile", 'post', "id", 'date']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Hashtag)
