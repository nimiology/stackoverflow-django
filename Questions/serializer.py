from rest_framework import serializers

from Questions.models import *
from users.serializer import WalletSerializer, TechSerializer, CategorySerializer


class QuestionSerializer(serializers.ModelSerializer):
    profile = WalletSerializer(read_only=True, required=False)
    upVote = WalletSerializer(many=True, read_only=True)
    downVote = WalletSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        self.fields['tech'] = TechSerializer(read_only=True, many=True)
        return super(QuestionSerializer, self).to_representation(instance)


class AnswerSerializer(serializers.ModelSerializer):
    profile = WalletSerializer(read_only=True, required=False)
    question = QuestionSerializer(read_only=True, required=False)
    upVote = WalletSerializer(many=True, read_only=True)
    downVote = WalletSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
