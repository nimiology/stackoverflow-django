from rest_framework import serializers

from Posts.models import (
    Hashtag,
    Post,
    Comment, Media,
)
from users.serializer import WalletSerializer


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

    def validate(self, attrs):
        post = attrs.get('post')
        question = attrs.get('question')
        answer = attrs.get('answer')
        if answer and not post and not question:
            return super(MediaSerializer, self).validate(attrs)
        elif post and not answer and not question:
            return super(MediaSerializer, self).validate(attrs)
        elif question and not post and not answer:
            return super(MediaSerializer, self).validate(attrs)
        else:
            raise serializers.ValidationError('You can only submit just on a foreignkey')


class PostSerializer(serializers.ModelSerializer):
    like = WalletSerializer(many=True, read_only=True)
    profile = WalletSerializer(read_only=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['tag'] = WalletSerializer(many=True)
        self.fields['media'] = MediaSerializer(many=True, read_only=True)
        self.fields['hashtag'] = HashtagSerializer(many=True)
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
