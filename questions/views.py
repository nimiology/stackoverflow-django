from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView

from questions.models import Question, Answer
from questions.serializer import QuestionSerializer, AnswerSerializer
from posts.permission import IsItOwner


class QuestionAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        # Edit Question
        self.permission_classes = [IsItOwner]
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Edit Question
        self.permission_classes = [IsItOwner]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Delete Question
        self.permission_classes = [IsItOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = self.get_object()
        self.check_object_permissions(self.request, instance)
        return serializer.save(profile=instance.profile)

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        return instance.delete()


class QuestionUpVote(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def post(self, request, *args, **kwargs):
        # upvote question
        profile = request.user
        question = self.get_object()
        if not profile in question.upVote.all():
            if profile in question.downVote.all():
                question.downVote.remove(profile)
            question.upVote.add(profile)
        else:
            question.upVote.remove(profile)
        return self.retrieve(request, *args, **kwargs)


class QuestionDownVote(QuestionUpVote):
    def post(self, request, *args, **kwargs):
        # downvote question
        profile = request.user
        question = self.get_object()
        if not profile in question.downVote.all():
            if profile in question.upVote.all():
                question.upVote.remove(profile)
            question.downVote.add(profile)
        else:
            question.downVote.remove(profile)
        return self.retrieve(request, *args, **kwargs)


class AnswerAPI(RetrieveUpdateDestroyAPIView):
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

    def perform_update(self, serializer):
        instance = self.get_object()
        self.check_object_permissions(self.request, instance)
        return serializer.save(profile=instance.profile, question=instance.question)

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        return instance.delete()


class AnswersListAPI(ListCreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    filterset_fields = {
        'profile': ['exact'],
        'question': ['exact'],
        'text': ['exact', 'contains'],
        'upVote': ['contains'],
        'downVote': ['contains'],
        'date': ['contains', 'exact', 'lte', 'gte'],

    }
    ordering_fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        profile = self.request.user
        return serializer.save(profile=profile)


class AnswerUpVote(QuestionUpVote):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'pk'


class AnswerDownVote(QuestionDownVote):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'pk'


class QuestionsListAPI(ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filterset_fields = {
        'profile': ['exact'],
        'title': ['exact', 'contains'],
        'text': ['exact', 'contains'],
        'slug': ['exact', 'contains'],
        'categories': ['contains'],
        'techs': ['contains'],
        'upVote': ['contains'],
        'downVote': ['contains'],
        'date': ['contains', 'exact', 'lte', 'gte'],

    }
    ordering_fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        profile = self.request.user
        return serializer.save(profile=profile)
