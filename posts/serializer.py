from djoser.serializers import UserSerializer
from rest_framework import serializers

from posts.models import Hashtag, Post, Comment


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True, required=False)
    like = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['tag'] = UserSerializer(many=True)
        self.fields['hashtag'] = HashtagSerializer(many=True)
        return super(PostSerializer, self).to_representation(instance)


class CommentSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    like = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['tag'] = UserSerializer(read_only=True, many=True)
        return super(CommentSerializer, self).to_representation(instance)
