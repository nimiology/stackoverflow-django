from djoser.serializers import UserSerializer
from rest_framework import serializers

from questions.models import *
from users.serializer import TechSerializer, CategorySerializer


class QuestionSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True, required=False)
    upVote = UserSerializer(many=True, read_only=True)
    downVote = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        self.fields['tech'] = TechSerializer(read_only=True, many=True)
        return super(QuestionSerializer, self).to_representation(instance)


class AnswerSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True, required=False)
    question = serializers.SlugRelatedField(slug_field='slug', queryset=Question.objects.all())
    upVote = UserSerializer(many=True, read_only=True)
    downVote = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['question'] = QuestionSerializer(read_only=True)
        return super(AnswerSerializer, self).to_representation(instance)