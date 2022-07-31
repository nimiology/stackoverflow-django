from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from questions.models import Question, Answer
from posts.tests import UserToken


class QuestionTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser = UserToken('testman')
        self.question = Question.objects.create(profile=self.user, title='test', text='asdf')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser)

    def test_create_request(self):
        response = self.client.post(reverse('question:questions_list'),
                                    data={'title': 'test', 'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(reverse('question:question', args=(self.question.slug,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_request(self):
        response = self.client.put(reverse('question:question', args=(self.question.slug,)),

                                   data={'title': 'test', 'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request(self):
        response = self.client.delete(reverse('question:question', args=(self.question.slug,)), )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upvote_request(self):
        response = self.client.post(reverse('question:upvote_question', args=(self.question.slug,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_downvote_request(self):
        response = self.client.post(reverse('question:downvote_question', args=(self.question.slug,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_questions_request(self):
        response = self.client.get(reverse('question:questions_list'), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AnswerTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser = UserToken('testman')
        self.question = Question.objects.create(profile=self.user, title='test', text='asdf')
        self.answer = Answer.objects.create(profile=self.user, question=self.question, text='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser)

    def test_create_answer(self):
        response = self.client.post(reverse('question:answers_list', ),
                                    data={'text': 'test', 'question': self.question.slug})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_question_answer(self):
        response = self.client.get(reverse('question:answers_list', ), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_answer(self):
        response = self.client.get(reverse('question:answer', args=(self.answer.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_answer(self):
        response = self.client.patch(reverse('question:answer', args=(self.answer.pk,)),
                                     data={'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_answer(self):
        response = self.client.delete(reverse('question:answer', args=(self.answer.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upvote_request(self):
        response = self.client.post(reverse('question:upvote_answer', args=(self.answer.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_downvote_request(self):
        response = self.client.post(reverse('question:downvote_answer', args=(self.answer.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
