import datetime

import jwt
from decouple import config
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Wallet, Industries, Tech, Job, Category, Company, CompanyDocument, Employee, WorkExperience, \
    Achievement, EducationalBackground


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


class CompanyDocumentTest(APITestCase):
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
        self.company = Company(profile=self.user1, companyName='test')
        self.company.save()
        self.companyDocument = CompanyDocument(company=self.company, document='static_cdn/media_root/test.jpg')
        self.companyDocument.save()

    # def test_create_company_document(self):
    #     response = self.client.post('/companydocument', HTTP_AUTHORIZATION=self.tokenUser1,
    #                                 files={'document': open('static_cdn/media_root/test.jpg', 'rb')},)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_edit_company_document(self):
    #     response = self.client.put(f'/companydocument/{self.companyDocument.pk}', HTTP_AUTHORIZATION=self.tokenUser1,
    #                                 files={'document': open('static_cdn/media_root/test.jpg', 'rb')})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_company_document(self):
        response = self.client.get(f'/companydocument/{self.companyDocument.pk}', HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_company_document(self):
        response = self.client.delete(f'/companydocument/{self.companyDocument.pk}',
                                      HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_accept_company_document(self):
        response = self.client.post(f'/company/{self.company.profile.username}/accept',
                                    HTTP_AUTHORIZATION=self.tokenAdmin, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_company_documents(self):
        response = self.client.get(f'/company/{self.company.profile.username}/companydocument',
                                   HTTP_AUTHORIZATION=self.tokenAdmin, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reject_company_document(self):
        response = self.client.post(f'/company/{self.company.profile.username}/reject',
                                    HTTP_AUTHORIZATION=self.tokenAdmin, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkExperienceTest(APITestCase):
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
        self.workExperience = WorkExperience(profile=self.user1, title='test', company='company', start='2020-10-10')
        self.workExperience.save()

    def test_create_work_experience(self):
        response = self.client.post('/workexperience', HTTP_AUTHORIZATION=self.tokenUser1,
                                    data={'title': 'test', 'company': 'company', 'start': '2020-1-1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_work_experience(self):
        response = self.client.put(f'/workexperience/{self.workExperience.pk}', HTTP_AUTHORIZATION=self.tokenUser1,
                                   data={'title': 'test', 'company': 'company1', 'start': '2020-1-1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_work_experience(self):
        response = self.client.get(f'/workexperience/{self.workExperience.pk}', HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_work_experience(self):
        response = self.client.delete(f'/workexperience/{self.workExperience.pk}', HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_work_experiences(self):
        response = self.client.get(f'/user/{self.user1.username}/workexperience',
                                   HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AchievementTest(APITestCase):
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
        self.achievement = Achievement(profile=self.user1, title='test', certificateProvider='company',
                                       date='2020-10-10')
        self.achievement.save()

    def test_create_work_experience(self):
        response = self.client.post('/achievement', HTTP_AUTHORIZATION=self.tokenUser1,
                                    data={'title': 'test', 'certificateProvider': 'company', 'date': '2020-1-1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_work_experience(self):
        response = self.client.put(f'/achievement/{self.achievement.pk}', HTTP_AUTHORIZATION=self.tokenUser1,
                                   data={'title': 'test', 'certificateProvider': 'company1', 'date': '2020-1-1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_work_experience(self):
        response = self.client.get(f'/achievement/{self.achievement.pk}', HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_work_experience(self):
        response = self.client.delete(f'/achievement/{self.achievement.pk}', HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_work_experiences(self):
        response = self.client.get(f'/user/{self.achievement.profile.username}/achievement',
                                   HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EducationalBackgroundTest(APITestCase):
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
        self.employee = Employee(profile=self.user1, name='test')
        self.employee.save()
        self.educationalBackground = EducationalBackground(profile=self.employee, educationalInstitute='institute',
                                                           major='test', grad='11', start='2020-10-10', adjusted=19.00)
        self.educationalBackground.save()

    def test_create_work_experience(self):
        response = self.client.post('/educationalbackground', HTTP_AUTHORIZATION=self.tokenUser1,
                                    data={'title': 'test', 'educationalInstitute': 'company',
                                          'major': 'test', 'grad': 'test', 'start': '2020-1-1',
                                          'adjusted': 19.00})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_work_experience(self):
        response = self.client.put(f'/educationalbackground/{self.educationalBackground.pk}',
                                   HTTP_AUTHORIZATION=self.tokenUser1,
                                   data={'title': 'test', 'educationalInstitute': 'company',
                                         'major': 'test', 'grad': 'test', 'start': '2020-1-1',
                                         'adjusted': 19.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_work_experience(self):
        response = self.client.get(f'/educationalbackground/{self.educationalBackground.pk}',
                                   HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_work_experience(self):
        response = self.client.delete(f'/educationalbackground/{self.educationalBackground.pk}',
                                      HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_work_experiences(self):
        response = self.client.get(f'/user/{self.educationalBackground.profile.profile.username}/educationalbackground',
                                   HTTP_AUTHORIZATION=self.tokenUser1, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
