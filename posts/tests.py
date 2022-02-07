from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from posts.models import Post, Comment, Hashtag
from users.models import MyUser


def UserToken(username):
    user = MyUser(username=username, password='1234')
    user.save()
    refresh = RefreshToken.for_user(user)
    return user, f'Bearer {refresh.access_token}'


class PostTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser = UserToken('testman')
        self.post = Post(profile=self.user)
        self.post.save()

    def test_create_request(self):
        response = self.client.post(reverse('post:create_post'), HTTP_AUTHORIZATION=self.tokenUser,
                                    data={'description': 'test1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(reverse('post:post', args=(self.post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_request(self):
        response = self.client.put(reverse('post:post', args=(self.post.slug,)), HTTP_AUTHORIZATION=self.tokenUser,
                                   data={'description': 'test1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request(self):
        response = self.client.delete(reverse('post:post', args=(self.post.slug,)), HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_users_post_request(self):
        response = self.client.get(reverse('post:user_post', args=(self.user.username,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_see_post_request(self):
        response = self.client.get(reverse('post:see_post'), HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_request(self):
        response = self.client.post(reverse('post:post_like', args=(self.post.slug,)),
                                    HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser = UserToken('testman')
        self.post = Post(profile=self.user)
        self.post.save()
        self.comment = Comment(profile=self.user, post=self.post, text='test')
        self.comment.save()

    def test_create_request(self):
        response = self.client.post(reverse('post:create_comment', args=(self.post.slug,)),
                                    HTTP_AUTHORIZATION=self.tokenUser, data={'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(reverse('post:comment', args=(self.comment.pk,)),
                                   HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request(self):
        response = self.client.delete(reverse('post:comment', args=(self.comment.pk,)),
                                      HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_like_request(self):
        response = self.client.post(reverse('post:comment_like', args=(self.comment.pk,)),
                                    HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_comment(self):
        response = self.client.get(reverse('post:post_comments', args=(self.comment.post.slug,)),
                                   HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HashtagTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser = UserToken('testman')
        self.hashtag = Hashtag(title='test')
        self.hashtag.save()
        self.post = Post(profile=self.user)
        self.post.save()

    def test_create_hashtag(self):
        response = self.client.post(reverse('post:create_hashtag'), HTTP_AUTHORIZATION=self.tokenUser,
                                    data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_hashtag(self):
        response = self.client.get(reverse('post:hashtag', args=(self.hashtag.pk,)),
                                   HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_hashtag_post(self):
        response = self.client.get(reverse('post:hashtag_posts', args=(self.hashtag.pk,)),
                                   HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_hashtags(self):
        response = self.client.get(reverse('post:hashtags'), HTTP_AUTHORIZATION=self.tokenUser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
