import datetime

import jwt
from decouple import config
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Wallet, Industries, Tech, Job, Category


class WalletTest(APITestCase):
    def setUp(self):
        self.tokenAdmin = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': 'ee8ac4bc-6bd1-4d80-956f-f6589ad9e691',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.tokenUser1 = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': '123e4567-e89b-12d3-a456-426614174000',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.user1 = Wallet(id='123e4567-e89b-12d3-a456-426614174000', username='test')
        self.user1.save()
        self.user2 = Wallet(id='123e4567-e89b-12d3-a456-426614174100', username='test2')
        self.user2.save()

    def test_get_wallet(self):
        response = self.client.get(f'/wallet/{self.user1.pk}', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_wallet(self):
        response = self.client.delete(f'/wallet/{self.user1.pk}', HTTP_AUTHORIZATION=self.tokenAdmin)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_follow_wallet(self):
        response = self.client.post(f'/follow/{self.user2.pk}', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_following_wallet(self):
        response = self.client.get(f'/user/{self.user2.pk}/following', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follower_wallet(self):
        response = self.client.get(f'/user/{self.user2.pk}/follower', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class IndustryTest(APITestCase):
    def setUp(self):
        self.tokenAdmin = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': 'ee8ac4bc-6bd1-4d80-956f-f6589ad9e691',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.tokenUser1 = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': '123e4567-e89b-12d3-a456-426614174000',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.user1 = Wallet(id='123e4567-e89b-12d3-a456-426614174000', username='test')
        self.user1.save()
        self.industry = Industries(title='test')
        self.industry.save()

    def test_create_industry(self):
        response = self.client.post('/industry', HTTP_AUTHORIZATION=self.tokenUser1,
                                    data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_industry(self):
        response = self.client.put(f'/industry/{self.industry.pk}', HTTP_AUTHORIZATION=self.tokenAdmin,
                                   data={'status': 'a'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_industry(self):
        response = self.client.get(f'/industry/{self.industry.pk}', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_industry(self):
        response = self.client.delete(f'/industry/{self.industry.pk}', HTTP_AUTHORIZATION=self.tokenAdmin,
                                      data={'status': 'a'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_industries(self):
        response = self.client.get(f'/industries', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TechTest(APITestCase):
    def setUp(self):
        self.tokenAdmin = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': 'ee8ac4bc-6bd1-4d80-956f-f6589ad9e691',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.tokenUser1 = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': '123e4567-e89b-12d3-a456-426614174000',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.user1 = Wallet(id='123e4567-e89b-12d3-a456-426614174000', username='test')
        self.user1.save()
        self.industry = Industries(title='test')
        self.industry.save()
        self.tech = Tech(title='test', industry=self.industry)
        self.tech.save()

    def test_create_tech(self):
        response = self.client.post('/tech', HTTP_AUTHORIZATION=self.tokenUser1,
                                    data={'title': 'test2', 'industry': self.industry.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_tech(self):
        response = self.client.put(f'/tech/{self.tech.pk}', HTTP_AUTHORIZATION=self.tokenAdmin,
                                   data={'status': 'a', 'industry': self.industry.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tech(self):
        response = self.client.get(f'/tech/{self.tech.pk}', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tech(self):
        response = self.client.delete(f'/tech/{self.tech.pk}', HTTP_AUTHORIZATION=self.tokenAdmin,
                                      data={'status': 'a'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_techs(self):
        response = self.client.get(f'/techs', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class JobTest(APITestCase):
    def setUp(self):
        self.tokenAdmin = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': 'ee8ac4bc-6bd1-4d80-956f-f6589ad9e691',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.tokenUser1 = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': '123e4567-e89b-12d3-a456-426614174000',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.user1 = Wallet(id='123e4567-e89b-12d3-a456-426614174000', username='test')
        self.user1.save()
        self.industry = Industries(title='test')
        self.industry.save()
        self.job = Job(title='test', industry=self.industry)
        self.job.save()

    def test_create_job(self):
        response = self.client.post('/job', HTTP_AUTHORIZATION=self.tokenUser1,
                                    data={'title': 'test2', 'industry': self.industry.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_job(self):
        response = self.client.put(f'/job/{self.job.pk}', HTTP_AUTHORIZATION=self.tokenAdmin,
                                   data={'title': 'a', 'industry': self.industry.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_job(self):
        response = self.client.get(f'/job/{self.job.pk}', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_job(self):
        response = self.client.delete(f'/job/{self.job.pk}', HTTP_AUTHORIZATION=self.tokenAdmin,
                                      data={'status': 'a'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_jobs(self):
        response = self.client.get(f'/jobs', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryTest(APITestCase):
    def setUp(self):
        self.tokenAdmin = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': 'ee8ac4bc-6bd1-4d80-956f-f6589ad9e691',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.tokenUser1 = jwt.encode(
            {'id': 'facf7b2d-4632-4c13-9ac0-75004a07ca16', 'role': 'admin', 'service': config('SERVICE_ID'),
             'packet_id': 'a5c3f752-bbba-4c4c-ac1f-bbe1b50b0efd', 'username': 'admin',
             'wallet_id': '123e4567-e89b-12d3-a456-426614174000',
             'iat': datetime.datetime.now(), 'exp': datetime.datetime.now() + datetime.timedelta(days=1)},
            config('AUTH_SECRET_KEY'),
            algorithm='HS256')
        self.user1 = Wallet(id='123e4567-e89b-12d3-a456-426614174000', username='test')
        self.user1.save()
        self.industry = Industries(title='test')
        self.industry.save()
        self.category = Category(title='test', industry=self.industry)
        self.category.save()

    def test_create_category(self):
        response = self.client.post('/category', HTTP_AUTHORIZATION=self.tokenUser1,
                                    data={'title': 'test2', 'industry': self.industry.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_category(self):
        response = self.client.put(f'/category/{self.category.pk}', HTTP_AUTHORIZATION=self.tokenAdmin,
                                   data={'title': 'a', 'industry': self.industry.pk, 'status': 'a'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category(self):
        response = self.client.get(f'/category/{self.category.pk}', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        response = self.client.delete(f'/category/{self.category.pk}', HTTP_AUTHORIZATION=self.tokenAdmin,
                                      data={'status': 'a'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_categorys(self):
        response = self.client.get(f'/categorys', HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
