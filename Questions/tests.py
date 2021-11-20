import datetime

import jwt
from decouple import config
from rest_framework import status
from rest_framework.test import APITestCase

from Questions.models import Question, Answer
from users.models import Wallet


class QuestionTest(APITestCase):
    def setUp(self):
        self.tokenAdmin = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': 'ee8ac4bc-6bd1-4d80-956f-f6589ad9e691',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.tokenUser = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': '123e4567-e89b-12d3-a456-426614174000',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')

        self.user1 = Wallet(id='123e4567-e89b-12d3-a456-426614174000', username='test')
        self.user1.save()
        self.question = Question(profile=self.user1, title='test', text='asdf')
        self.question.save()

    def test_create_request(self):
        response = self.client.post('/question', HTTP_AUTHORIZATION=self.tokenUser,
                                    data={'title': 'test', 'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(f'/question/{self.question.slug}', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_request(self):
        response = self.client.put(f'/question/{self.question.slug}', HTTP_AUTHORIZATION=self.tokenUser,
                                   data={'title': 'test', 'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request(self):
        response = self.client.delete(f'/question/{self.question.slug}', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upvote_request(self):
        response = self.client.post(f'/question/{self.question.slug}/upvote', HTTP_AUTHORIZATION=self.tokenUser, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_downvote_request(self):
        response = self.client.post(f'/question/{self.question.slug}/downvote', HTTP_AUTHORIZATION=self.tokenUser, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_questions_request(self):
        response = self.client.get(f'/user/{self.user1.username}/question', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_questions_request(self):
        response = self.client.get(f'/questions', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class AnswerTest(APITestCase):
    def setUp(self):
        self.tokenAdmin = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': 'ee8ac4bc-6bd1-4d80-956f-f6589ad9e691',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.tokenUser = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': '123e4567-e89b-12d3-a456-426614174000',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')

        self.user1 = Wallet(id='123e4567-e89b-12d3-a456-426614174000', username='test')
        self.user1.save()
        self.question = Question(profile=self.user1, title='test', text='asdf')
        self.question.save()
        self.answer = Answer(profile=self.user1, question=self.question, text='test')
        self.answer.save()

    def test_create_answer(self):
        response = self.client.post(f'/question/{self.question.slug}/answer', HTTP_AUTHORIZATION=self.tokenUser,
                                    data={'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_answers_questions(self):
        response = self.client.get(f'/question/{self.question.slug}/answers', HTTP_AUTHORIZATION=self.tokenUser,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_answer(self):
        response = self.client.get(f'/answer/{self.answer.pk}', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_edit_answer(self):
        response = self.client.put(f'/answer/{self.answer.pk}', HTTP_AUTHORIZATION=self.tokenUser,
                                   data={'text':'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_answer(self):
        response = self.client.delete(f'/answer/{self.answer.pk}', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upvote_request(self):
        response = self.client.post(f'/answer/{self.answer.pk}/upvote', HTTP_AUTHORIZATION=self.tokenUser, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_downvote_request(self):
        response = self.client.post(f'/answer/{self.answer.pk}/downvote', HTTP_AUTHORIZATION=self.tokenUser, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)