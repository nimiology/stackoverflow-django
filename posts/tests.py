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
        self.post = Post.objects.create(profile=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser)

    def test_create_request(self):
        response = self.client.post(reverse('post:post'),
                                    data={'description': 'test1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(reverse('post:post', args=(self.post.slug,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_request(self):
        response = self.client.put(reverse('post:post', args=(self.post.slug,)),
                                   data={'description': 'test1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request(self):
        response = self.client.delete(reverse('post:post', args=(self.post.slug,)), )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_reqeust_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=UserToken('John')[1])
        response = self.client.delete(reverse('post:post', args=(self.post.slug,)), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_posts_list_request(self):
        response = self.client.get(reverse('post:posts_list', ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_see_post_request(self):
        response = self.client.get(reverse('post:see_post'), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_request(self):
        response = self.client.post(reverse('post:post_like', args=(self.post.slug,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser = UserToken('testman')
        self.post = Post.objects.create(profile=self.user)
        self.comment = Comment.objects.create(profile=self.user, post=self.post, text='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser)

    def test_create_request(self):
        response = self.client.post(reverse('post:comment', args=(self.post.slug,)),
                                    data={'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(reverse('post:comment', args=(self.comment.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_request(self):
        response = self.client.delete(reverse('post:comment', args=(self.comment.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_like_request(self):
        response = self.client.post(reverse('post:comment_like', args=(self.comment.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_comment(self):
        response = self.client.get(reverse('post:comments_list', ), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HashtagTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser = UserToken('testman')
        self.hashtag = Hashtag.objects.create(title='test')
        self.post = Post(profile=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser)

    def test_get_hashtag(self):
        response = self.client.get(reverse('post:hashtag', args=(self.hashtag.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_hashtag(self):
        response = self.client.get(reverse('post:hashtag', args=("test2",)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_hashtags(self):
        response = self.client.get(reverse('post:hashtags_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
