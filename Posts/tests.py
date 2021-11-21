import datetime

import jwt
from decouple import config
from rest_framework import status
from rest_framework.test import APITestCase

from Posts.models import Post, Comment, Hashtag, Media
from users.models import Wallet


class PostTest(APITestCase):
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
        self.post = Post(profile=self.user1)
        self.post.save()

    def test_create_request(self):
        response = self.client.post('/post', HTTP_AUTHORIZATION=self.tokenUser,
                                    data={'description': 'test1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(f'/post/{self.post.slug}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request(self):
        response = self.client.delete(f'/post/{self.post.slug}', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_users_post_request(self):
        response = self.client.get(f'/post/user/{self.user1.username}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_see_post_request(self):
        response = self.client.get(f'/seeposts', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_request(self):
        response = self.client.post(f'/post/{self.post.slug}/like', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentTest(APITestCase):
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
        self.post = Post(profile=self.user1)
        self.post.save()
        self.comment = Comment(profile=self.user1, post=self.post, text='test')
        self.comment.save()

    def test_create_request(self):
        response = self.client.post(f'/post/{self.post.slug}/comment', HTTP_AUTHORIZATION=self.tokenUser
                                    , data={'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(f'/comment/{self.comment.pk}', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request(self):
        response = self.client.delete(f'/comment/{self.comment.pk}', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_like_request(self):
        response = self.client.post(f'/comment/{self.comment.pk}/like', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_comment(self):
        response = self.client.get(f'/post/{self.post.slug}/comments', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HashtagTest(APITestCase):
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
        self.hashtag = Hashtag(title='test')
        self.hashtag.save()
        self.post = Post(profile=self.user1)
        self.post.save()

    def test_create_hashtag(self):
        response = self.client.post('/hashtag', HTTP_AUTHORIZATION=self.tokenUser,
                                    data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_hashtag(self):
        response = self.client.delete(f'/hashtag/{self.hashtag.pk}', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_hashtag_post(self):
        response = self.client.get(f'/hashtag/{self.hashtag.pk}/posts', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_hashtag(self):
        response = self.client.get(f'/hashtags', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MediaTest(APITestCase):
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
        self.post = Post(profile=self.user1)
        self.post.save()
        self.picture = 'static_cdn/media_root/test.jpg'
        self.media = Media(thumbnail=self.picture, media=self.picture, alt='test', post=self.post)
        self.media.save()

    def test_create_media(self):
        response = self.client.post('/media', files={'thumbnail': open(self.picture, 'rb'),
                                                     'media': open(self.picture, 'rb')},
                                    data={'alt': 'test', 'post': self.post.pk}, HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_media(self):
        response = self.client.put(f'/media/{self.media.pk}', files={'thumbnail': open(self.picture, 'rb'),
                                                                     'media': open(self.picture, 'rb')},
                                   data={'alt': 'test', 'post': self.post.pk}, HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_media(self):
        response = self.client.put(f'/media/{self.media.pk}', files={'thumbnail': open(self.picture, 'rb'),
                                                                     'media': open(self.picture, 'rb')},
                                   data={'alt': 'test', 'post': self.post.pk}, HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_media(self):
        response = self.client.delete(f'/media/{self.media.pk}', HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
