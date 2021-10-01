from django.http import Http404
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   ListModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin)
from rest_framework.response import Response
from rest_framework.views import APIView

from Posts.serializer import *
from authentication.permission import BlockedByUserWithPost
from users.utils import GetWallet, VerifyToken, CheckAdmin
from rest_framework.exceptions import ValidationError


def GetObject(obj, slug):
    try:
        post = obj.objects.get(slug=slug)
    except obj.DoesNotExist:
        raise Http404
    return post


def CheckBlock(profile, post):
    if not (profile in post.profile.block.all()):
        return False
    else:
        raise ValidationError("You've been blocked!")


def get_object_by_id(cl, id):
    try:
        return cl.objects.get(id=id)
    except cl.DoesNotExist:
        raise Http404


class PostAPI(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [BlockedByUserWithPost]

    def get(self, request, *args, **kwargs):
        """Get Post"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Post"""
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Post"""
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        wallet = GetWallet(self.request)
        """Is there any pic or description?"""
        if 'pic' in self.request.data:
            if self.request.data['pic'] == '' and 'description' not in self.request.data:
                raise ValidationError('You should give me one of pic or description or both')
        if 'description' in self.request.data:
            if self.request.data['description'] == '':
                raise ValidationError('You should give me one of pic or description or both')
        if 'pic' in self.request.data or 'description' in self.request.data:
            return serializer.save(profile=wallet)
        else:
            raise ValidationError('You should give me one of pic or description or both')

    def perform_destroy(self, instance):
        """Is he him?"""
        if instance.profile == GetWallet(self.request):
            return instance.delete()
        else:
            raise ValidationError('access denied!')


class UserPostsAPI(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get all User's Post"""
        authID = self.kwargs['slug']
        owner = Wallet.objects.get(id=authID)
        profile = GetWallet(self.request)
        if not (profile in owner.block.all()):
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
        posts = Post.objects.order_by('-date').filter(profile__in=profile.following.all())
        return posts


class Like(APIView):
    def post(self, request, *args, **kwargs):
        """Like"""
        slug = kwargs['slug']
        profile = GetWallet(request)
        post = GetObject(Post, slug)
        CheckBlock(profile, post)
        post.like.add(profile)
        data = PostSerializer(post).data
        return Response(data, status=status.HTTP_200_OK)


class CommentAPI(CreateModelMixin, RetrieveModelMixin,
                 UpdateModelMixin, DestroyModelMixin,
                 GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Comment"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Comment"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Comment"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Comment"""
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        wallet = GetWallet(self.request)
        post = GetObject(Post, self.kwargs['slug'])
        CheckBlock(wallet, post)
        if 'replyToComment' in self.request.data:
            replyTOComment = get_object_by_id(Comment, self.request.data['replyToComment'])
            replyToCommentPost = replyTOComment.post.id
            if replyToCommentPost != post:
                raise ValidationError("Upper comment didn't found")
        return serializer.save(profile=wallet, post=post)

    def perform_destroy(self, instance):
        """Is he him?"""
        if instance.profile == GetWallet(self.request) or instance.profile == instance.post.profile:
            return instance.delete()
        else:
            raise ValidationError('access denied!')
    # def perform_update(self, serializer):
    #     wallet = GetWallet(self.request)
    #     comment = GetObject(Comment, self.kwargs['id'])
    #     if comment.profile.id == wallet.id:
    #         comment.profile = comment.profile
    #         comment.post = comment.post
    #         if comment.replyToComment:
    #             comment.replyToComment = comment.replyToComment.id
    #         if comment.tag:
    #             comment.tag = comment.tag.id
    #     else:
    #         raise ValidationError
    #
    #     return serializer.save(profile=wallet, post=post)
