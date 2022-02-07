from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from questions.models import Question, Answer
from posts.tests import UserToken


class QuestionTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser = UserToken('testman')
        self.question = Question(profile=self.user, title='test', text='asdf')
        self.question.save()

    def test_create_request(self):
        response = self.client.post(reverse('question:create_question'), HTTP_AUTHORIZATION=self.tokenUser,
                                    data={'title': 'test', 'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(reverse('question:question', args=(self.question.slug,)),
                                   HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_request(self):
        response = self.client.put(reverse('question:question', args=(self.question.slug,)),
                                   HTTP_AUTHORIZATION=self.tokenUser,
                                   data={'title': 'test', 'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request(self):
        response = self.client.delete(reverse('question:question', args=(self.question.slug,)),
                                      HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upvote_request(self):
        response = self.client.post(reverse('question:upvote_question', args=(self.question.slug,)),
                                    HTTP_AUTHORIZATION=self.tokenUser, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_downvote_request(self):
        response = self.client.post(reverse('question:downvote_question', args=(self.question.slug,)),
                                    HTTP_AUTHORIZATION=self.tokenUser, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_questions_request(self):
        response = self.client.get(reverse('question:user_questions', args=(self.user.username,)),
                                   HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_questions_request(self):
        response = self.client.get(reverse('question:questions'),
                                   HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AnswerTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser = UserToken('testman')
        self.question = Question(profile=self.user, title='test', text='asdf')
        self.question.save()
        self.answer = Answer(profile=self.user, question=self.question, text='test')
        self.answer.save()

    def test_create_answer(self):
        response = self.client.post(reverse('question:create_answer', args=(self.question.slug,)),
                                    HTTP_AUTHORIZATION=self.tokenUser,
                                    data={'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_question_answer(self):
        response = self.client.get(reverse('question:question_answers', args=(self.question.slug,)),
                                   HTTP_AUTHORIZATION=self.tokenUser, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_answer(self):
        response = self.client.get(reverse('question:answer', args=(self.answer.pk,)),
                                   HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_answer(self):
        response = self.client.put(reverse('question:answer', args=(self.answer.pk,)),
                                   HTTP_AUTHORIZATION=self.tokenUser,
                                   data={'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_answer(self):
        response = self.client.delete(reverse('question:answer', args=(self.answer.pk,)),
                                      HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upvote_request(self):
        response = self.client.post(reverse('question:upvote_answer', args=(self.answer.pk,)),
                                    HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_downvote_request(self):
        response = self.client.post(reverse('question:downvote_answer', args=(self.answer.pk,)),
                                    HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
