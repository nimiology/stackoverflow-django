from rest_framework import serializers

from Posts.models import (
    Hashtag,
    Post,
    Comment,
)
from users.serializer import WalletSerializer


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    like = WalletSerializer(many=True, read_only=True)
    profile = WalletSerializer(read_only=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['tag'] = WalletSerializer(many=True, required=False)
        self.fields['hashtag'] = HashtagSerializer(many=True, required=False)
        return super(PostSerializer, self).to_representation(instance)


class CommentSerializer(serializers.ModelSerializer):
    profile = WalletSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    like = WalletSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['tag'] = WalletSerializer(read_only=True, many=True)
        return super(CommentSerializer, self).to_representation(instance)
