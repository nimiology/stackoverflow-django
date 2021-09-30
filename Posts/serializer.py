from rest_framework import serializers

from Posts.models import *
from users.serializer import ProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        self.fields['tag'] = ProfileSerializer(many=True, read_only=True)
        self.fields['like'] = ProfileSerializer(many=True, read_only=True)
        return super(PostSerializer, self).to_representation(instance)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        self.fields['post'] = PostSerializer(read_only=True)
        self.fields['tag'] = ProfileSerializer(read_only=True)
        self.fields['like'] = ProfileSerializer(many=True, read_only=True)
        return super(CommentSerializer, self).to_representation(instance)


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'
