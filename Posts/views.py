from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView

from Posts.serializer import *
from Posts.permission import IsItOwner
from rest_framework.exceptions import ValidationError
from Posts.utils import CreateRetrieveUpdateDestroyAPIView
from users.models import UserInfo


class PostAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        self.permission_classes = [IsItOwner]
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.permission_classes = [IsItOwner]
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Delete Post
        self.permission_classes = [IsItOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(profile=user)

    def perform_update(self, serializer):
        user = self.request.user
        return serializer.save(profile=user)

    def perform_destroy(self, instance):
        self.check_object_permissions(obj=instance, request=self.request)
        return instance.delete()


class UserPostsAPI(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get all User's Post
        username = self.kwargs['slug']
        owner = UserInfo.objects.get(username=username)
        qs = owner.post.all()
        return qs


class SeePosts(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get Posts
        profile = self.request.user
        posts = Post.objects.filter(profile__in=profile.userInfo.following.all()).order_by('-date')
        return posts


class Like(APIView):
    def post(self, request, *args, **kwargs):
        # Like
        slug = kwargs['slug']
        profile = request.user
        post = get_object_or_404(Post, slug=slug)
        if not profile in post.like.all():
            post.like.add(profile)
        else:
            post.like.remove(profile)
        data = PostSerializer(post).data
        return Response(data, status=status.HTTP_200_OK)


class CommentAPI(CreateAPIView, RetrieveAPIView, DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def delete(self, request, *args, **kwargs):
        # Delete Comment
        self.permission_classes = [IsItOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        if 'replyToComment' in self.request.data:
            replyTOComment = get_object_or_404(Comment, id=self.request.data['replyToComment'])
            replyToCommentPost = replyTOComment.post.id
            if replyToCommentPost != post:
                raise ValidationError("Upper comment didn't found")
        return serializer.save(profile=user, post=post)

    def perform_destroy(self, instance):
        # Is he him?
        self.check_object_permissions(obj=instance, request=self.request)
        return instance.delete()


class CommentLike(APIView):
    def post(self, request, *args, **kwargs):
        # Like
        id = kwargs['pk']
        profile = request.user
        comment = get_object_or_404(Comment, id=id)
        if not profile in comment.like.all():
            comment.like.add(profile)
        else:
            comment.like.remove(profile)
        data = CommentSerializer(comment).data
        return Response(data, status=status.HTTP_200_OK)


class PostCommentsAPI(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Get Post's Comments
        slug = self.kwargs['slug']
        post = get_object_or_404(Post, slug=slug)
        qs = post.comment.all()
        return qs


class HashtagAPI(CreateAPIView, RetrieveAPIView):
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()


class AllHashtagsAPI(ListAPIView):
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()
    filterset_fields = ['title']


class HashtagPostAPI(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_object_or_404(Hashtag, pk=self.kwargs['id']).post.all()
