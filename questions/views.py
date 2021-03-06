import django_filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, get_object_or_404

from posts.utils import CreateRetrieveUpdateDestroyAPIView
from questions.models import Question, Answer
from questions.serializer import QuestionSerializer, AnswerSerializer
from posts.permission import IsItOwner


class QuestionAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        # Edit Question
        self.permission_classes = [IsItOwner]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Delete Question
        self.permission_classes = [IsItOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        profile = self.request.user
        return serializer.save(profile=profile)

    def perform_update(self, serializer):
        instance = get_object_or_404(Question, slug=self.kwargs['slug'])
        self.check_object_permissions(self.request, instance)
        return serializer.save(profile=instance.profile)

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        return instance.delete()


class AllUserQuestionsAPI(ListAPIView):
    serializer_class = QuestionSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['title', 'text']

    def get_queryset(self):
        username = self.kwargs['slug']
        qs = Question.objects.filter(profile__username=username)
        return qs


class QuestionUpVote(APIView):
    def post(self, request, *args, **kwargs):
        # upvote question"""
        slug = kwargs['slug']
        profile = request.user
        question = get_object_or_404(Question, slug=slug)
        if not profile in question.upVote.all():
            if profile in question.downVote.all():
                question.downVote.remove(profile)
            question.upVote.add(profile)
        else:
            question.upVote.remove(profile)
        data = QuestionSerializer(question).data
        return Response(data, status=status.HTTP_200_OK)


class QuestionDownVote(APIView):
    def post(self, request, *args, **kwargs):
        # downvote question
        slug = kwargs['slug']
        profile = request.user
        question = get_object_or_404(Question, slug=slug)
        if not profile in question.downVote.all():
            if profile in question.upVote.all():
                question.upVote.remove(profile)
            question.downVote.add(profile)
        else:
            question.downVote.remove(profile)
        data = QuestionSerializer(question).data
        return Response(data, status=status.HTTP_200_OK)


class AnswerAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def put(self, request, *args, **kwargs):
        # Edit Answer
        self.permission_classes = [IsItOwner]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Delete Answer
        self.permission_classes = [IsItOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        profile = self.request.user
        slug = self.kwargs['slug']
        question = get_object_or_404(Question, slug=slug)
        return serializer.save(profile=profile, question=question)

    def perform_update(self, serializer):
        instance = get_object_or_404(Answer, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, instance)
        return serializer.save(profile=instance.profile, question=instance.question)

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        return instance.delete()


class QuestionAnswers(ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        # Get QuestionAnswer
        question = get_object_or_404(Question, slug=self.kwargs['slug'])
        qs = question.answer.all()
        return qs


class AnswerUpVote(APIView):
    def post(self, request, *args, **kwargs):
        # upvote Answer
        id = kwargs['pk']
        profile = request.user
        answer = get_object_or_404(Answer, id=id)
        if not profile in answer.upVote.all():
            if profile in answer.downVote.all():
                answer.downVote.remove(profile)
            answer.upVote.add(profile)
        else:
            answer.upVote.remove(profile)
        data = AnswerSerializer(answer).data
        return Response(data, status=status.HTTP_200_OK)


class AnswerDownVote(APIView):
    def post(self, request, *args, **kwargs):
        # downvote Answer
        id = kwargs['pk']
        profile = request.user
        answer = get_object_or_404(Answer, id=id)
        if not profile in answer.downVote.all():
            if profile in answer.upVote.all():
                answer.upVote.remove(profile)
            answer.downVote.add(profile)
        else:
            answer.downVote.remove(profile)
        data = AnswerSerializer(answer).data
        return Response(data, status=status.HTTP_200_OK)


class SearchQuestions(ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('-date')
    filterset_fields = ['title', 'text', 'category', 'tech']
