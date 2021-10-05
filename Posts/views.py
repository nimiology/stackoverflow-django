from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    get_object_or_404,
)
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from Posts.serializer import *
from Posts.permission import (
    BlockedByUserWithPost,
    CheckBlock,
    IsItOwner,
    IsItPostOwner,
    IsAdmin,
    IsRequestMethodDelete,
    IsRequestMethodPost,
    DeleteObjectByAdminOrOwner,
    IsPrivate,
    IsPrivateWithPost,
)
from users.utils import GetWallet
from rest_framework.exceptions import ValidationError
from Posts.utils import StandardResultsSetPagination
from users.models import Wallet


class PostAPI(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [BlockedByUserWithPost & IsPrivateWithPost, IsItOwner]

    def get(self, request, *args, **kwargs):
        """Get Post"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Post"""
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Post"""
        self.permission_classes = [DeleteObjectByAdminOrOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        wallet = GetWallet(self.request)
        """Is there any pic or description?"""
        if 'pic' in self.request.data:
            if self.request.data['pic'] == '' and 'description' not in self.request.data:
                raise ValidationError(
                    'You should give me one of pic or description or both')
        if 'description' in self.request.data:
            if self.request.data['description'] == '':
                raise ValidationError(
                    'You should give me one of pic or description or both')
        if 'pic' in self.request.data or 'description' in self.request.data:
            return serializer.save(profile=wallet)
        else:
            raise ValidationError(
                'You should give me one of pic or description or both')

    def perform_destroy(self, instance):
        """Is he him?"""
        self.check_object_permissions(obj=instance, request=self.request)
        return instance.delete()


class UserPostsAPI(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get all User's Post"""
        authID = self.kwargs['slug']
        owner = Wallet.objects.get(id=authID)
        profile = GetWallet(self.request)
        if not (profile in owner.block.all()):
            if owner.private:
                if owner in profile.following.all():
                    qs = owner.post.all()
                    return qs
                else:
                    raise ValidationError('This page is private')
            else:
                qs = owner.post.all()
                return qs
        else:
            raise ValidationError("You've been blocked")


class SeePosts(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get Posts"""
        profile = GetWallet(self.request)
        posts = Post.objects.order_by(
            '-date').filter(profile__in=profile.following.all())
        return posts


class Like(APIView):
    def post(self, request, *args, **kwargs):
        """Like"""
        slug = kwargs['slug']
        profile = GetWallet(request)
        post = get_object_or_404(Post, slug=slug)
        if not (profile in post.profile.block.all()):
            if not profile in post.like.all():
                post.like.add(profile)
            else:
                post.like.remove(profile)
            data = PostSerializer(post).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("You've been blocked!")


class CommentAPI(CreateModelMixin, RetrieveModelMixin,
                 DestroyModelMixin, GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [CheckBlock]

    def get(self, request, *args, **kwargs):
        """Get Comment"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Comment"""
        self.permission_classes = [IsPrivate & CheckBlock]
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Comment"""
        self.permission_classes = [IsItPostOwner |
                                   DeleteObjectByAdminOrOwner | IsItOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        wallet = GetWallet(self.request)
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        self.check_object_permissions(self.request, post)
        if 'replyToComment' in self.request.data:
            replyTOComment = get_object_or_404(
                Comment, id=self.request.data['replyToComment'])
            replyToCommentPost = replyTOComment.post.id
            if replyToCommentPost != post:
                raise ValidationError("Upper comment didn't found")
        return serializer.save(profile=wallet, post=post)

    def perform_destroy(self, instance):
        """Is he him?"""
        self.check_object_permissions(obj=instance, request=self.request)
        return instance.delete()


class CommentLike(APIView):
    def post(self, request, *args, **kwargs):
        """Like"""
        id = kwargs['pk']
        profile = GetWallet(request)
        comment = get_object_or_404(Comment, id=id)
        if not (profile in comment.profile.block.all()):
            if not profile in comment.like.all():
                comment.like.add(profile)
            else:
                comment.like.remove(profile)
            data = CommentSerializer(comment).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("You've been blocked!")


class PostCommentsAPI(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [CheckBlock & IsPrivate]

    def get_queryset(self):
        """Get Post's Comments"""
        slug = self.kwargs['slug']
        post = get_object_or_404(Post, slug=slug)
        self.check_object_permissions(self.request, post)
        qs = post.comment.all()
        return qs


class HashtagAPI(GenericAPIView, CreateModelMixin, DestroyModelMixin):
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()
    permission_classes = [
        IsAdmin & IsRequestMethodDelete | IsRequestMethodPost]

    def post(self, request, *args, **kwargs):
        """Create Hashtag"""
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Hashtag By Admin"""
        return self.destroy(request, *args, **kwargs)


class AllHashtagAPI(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Hashtag.objects.all()
    filter_backends = [DjangoFilterBackend]
    """Search Fields"""
    filterset_fields = ['title']


class HashtagPostAPI(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get Hashtag's Post"""
        hashtag = get_object_or_404(Hashtag, id=self.kwargs['pk'])
        qs = hashtag.post.all()
        return qs
