from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, DestroyAPIView

from posts.serializer import *
from posts.permission import IsItOwner
from rest_framework.exceptions import ValidationError


class PostAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
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

    def perform_update(self, serializer):
        user = self.request.user
        return serializer.save(profile=user)


class PostsListAPI(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filterset_fields = {'profile': ['exact'],
                        'slug': ['contains', 'exact'],
                        'tags': ['contains'],
                        'description': ['contains', 'exact'],
                        'hashtags': ['contains'],
                        'likes': ['contains'],
                        'date': ['contains', 'exact', 'lte', 'gte'],
                        }
    ordering_fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(profile=user)


class SeePosts(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get posts
        profile = self.request.user
        posts = Post.objects.filter(profile__in=profile.following.all()).order_by('-date')
        return posts


class PostLike(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def post(self, request, *args, **kwargs):
        profile = request.user
        post = self.get_object()
        if not profile in post.likes.all():
            post.likes.add(profile)
        else:
            post.likes.remove(profile)
        return self.retrieve(request, *args, **kwargs)


class CommentAPI(RetrieveAPIView, DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def delete(self, request, *args, **kwargs):
        # Delete Comment
        self.permission_classes = [IsItOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # Is he him?
        self.check_object_permissions(obj=instance, request=self.request)
        return instance.delete()


class CommentLike(PostLike):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'


class CommentsListAPI(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filterset_fields = {'profile': ['exact'],
                        'post': ['exact'],
                        'replyTo': ['exact'],
                        'tags': ['contains'],
                        'text': ['contains', 'exact'],
                        'likes': ['contains'],
                        'date': ['contains', 'exact', 'lte', 'gte'],
                        }
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(profile=user)


class HashtagAPI(RetrieveAPIView):
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset().get_or_create(title=kwargs['title'])[0]
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class HashtagsListAPI(ListAPIView):
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()
    filterset_fields = ['title']
    ordering_fields = '__all__'
