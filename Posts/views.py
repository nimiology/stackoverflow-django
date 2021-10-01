from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   ListModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin)

from Posts.serializer import *
from authentication.permission import BlockedByUserWithPost
from users.utils import GetWallet
from rest_framework.exceptions import ValidationError


class PostAPI(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [BlockedByUserWithPost]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        wallet = GetWallet(self.request)
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
        if instance.profile == GetWallet(self.request):
            return instance.delete()
        else:
            raise ValidationError('access denied!')


class UserPostsAPI(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        authID = self.kwargs['slug']
        owner = Wallet.objects.get(id=authID)
        profile = GetWallet(self.request)
        if not(profile in owner.block.all()):
            qs = owner.post.all()
            print(qs)
            return qs
        else:
            raise ValidationError("You've been blocked")


class SeePosts(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        profile = GetWallet(self.request)
        posts = Post.objects.order_by('-date').filter(profile__in=profile.following.all())
        return posts
