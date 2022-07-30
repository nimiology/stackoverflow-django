from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from posts.models import Hashtag, Post, Comment


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True, required=False)
    likes = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['tags'] = UserSerializer(many=True)
        self.fields['hashtags'] = HashtagSerializer(many=True)
        return super(PostSerializer, self).to_representation(instance)


class CommentSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True)
    post = serializers.SlugRelatedField(slug_field='slug', queryset=Post.objects.all())
    like = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        reply_to_comment = attrs.get('replyToComment')
        if reply_to_comment:
            if reply_to_comment.post.id != attrs.get('post'):
                raise ValidationError("Upper comment didn't found")
        return attrs

    def to_representation(self, instance):
        self.fields['tag'] = UserSerializer(read_only=True, many=True)
        self.fields['post'] = PostSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)
