from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from Questions.models import *
from users.serializer import ProfileSerializer, TechSerializer, CategorySerializer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        self.fields['questionSlug'] = ReadOnlyField(source='question.slug')
        self.fields['upVote'] = ProfileSerializer(many=True, read_only=True)
        self.fields['downVote'] = ProfileSerializer(many=True, read_only=True)
        return super(AnswerSerializer, self).to_representation(instance)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        self.fields['tech'] = TechSerializer(read_only=True, many=True)
        self.fields['answer'] = AnswerSerializer(many=True, read_only=True)
        self.fields['upVote'] = ProfileSerializer(many=True, read_only=True)
        self.fields['downVote'] = ProfileSerializer(many=True, read_only=True)
        return super(QuestionSerializer, self).to_representation(instance)