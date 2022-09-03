from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from posts.tests import UserToken
from users.models import MyUser, Industry, Tech, Job, Category, Company, Employee, WorkExperience, \
    Achievement, EducationalBackground, Notification, ApplyForJob, JobOffer


class UserTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.user2, self.tokenUser2 = UserToken('testman2')

    def test_get_wallet(self):
        response = self.client.get(reverse('users:wallet', args=(self.user1.username,)),
                                   HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_wallet(self):
        response = self.client.post(reverse('users:follow', args=(self.user2.username,)),
                                    HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_following_wallet(self):
        response = self.client.get(reverse('users:followings', args=(self.user1.username,)),
                                   HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follower_wallet(self):
        response = self.client.get(reverse('users:followers', args=(self.user1.username,)),
                                   HTTP_AUTHORIZATION=self.tokenUser1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class IndustryTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.industry = Industry.objects.create(title='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_create_industry(self):
        response = self.client.get(reverse('users:industry', args=('sadf',)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_industry(self):
        response = self.client.get(reverse('users:industry', args=(self.industry.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_industries(self):
        response = self.client.get(reverse('users:industries_list'), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TechTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.industry = Industry.objects.create(title='test')
        self.tech = Tech.objects.create(title='test', industry=self.industry)
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_create_tech(self):
        response = self.client.post(reverse('users:techs_list'),
                                    data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tech(self):
        response = self.client.get(reverse('users:tech', args=(self.tech.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_techs(self):
        response = self.client.get(reverse('users:techs_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.industry = Industry.objects.create(title='test')
        self.category = Category.objects.create(title='test', industry=self.industry)
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_get_category(self):
        response = self.client.get(reverse('users:category', args=(self.category.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_categories(self):
        response = self.client.get(reverse('users:categories_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class JobTest(APITestCase):
    def setUp(self):
        self.user, self.tokenUser1 = UserToken('testman1')
        self.industry = Industry.objects.create(title='test')
        self.job = Job.objects.create(title='test', industry=self.industry)
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_create_job(self):
        response = self.client.post(reverse('users:jobs_list'),
                                    data={'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_job(self):
        response = self.client.get(reverse('users:job', args=(self.job.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_jobs(self):
        response = self.client.get(reverse('users:jobs_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkExperienceTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.workExperience = WorkExperience.objects.create(profile=self.user1, title='test', company='company',
                                                            start='2020-10-10')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_create_work_experience(self):
        response = self.client.post(reverse('users:workexperiences_list'),
                                    data={'title': 'test', 'company': 'company', 'start': '2020-1-1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_work_experience(self):
        response = self.client.put(reverse('users:workexperience', args=(self.workExperience.pk,)),

                                   data={'title': 'test', 'company': 'company1', 'start': '2020-1-1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_work_experience(self):
        response = self.client.get(reverse('users:workexperience', args=(self.workExperience.pk,)),
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_work_experience(self):
        response = self.client.delete(reverse('users:workexperience', args=(self.workExperience.pk,)),
                                      )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_work_experiences(self):
        response = self.client.get(reverse('users:workexperiences_list', ),
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AchievementTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.achievement = Achievement.objects.create(profile=self.user1, title='test', certificateProvider='company',
                                                      date='2020-10-10')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_create_achievement(self):
        response = self.client.post(reverse('users:achievements_list'),
                                    data={'title': 'test', 'certificateProvider': 'company', 'date': '2020-1-1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_achievement(self):
        response = self.client.put(reverse('users:achievement', args=(self.achievement.pk,)),
                                   data={'title': 'test', 'certificateProvider': 'company1', 'date': '2020-1-1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_achievement(self):
        response = self.client.get(reverse('users:achievement', args=(self.achievement.pk,)),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_achievement(self):
        response = self.client.delete(reverse('users:achievement', args=(self.achievement.pk,)),)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_achievements(self):
        response = self.client.get(reverse('users:achievements_list', ),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EducationalBackgroundTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.employee = Employee.objects.create(profile=self.user1, name='test')
        self.educationalBackground = EducationalBackground.objects.create(profile=self.employee,
                                                                          educationalInstitute='institute',
                                                                          major='test', grad='11', start='2020-10-10',
                                                                          adjusted=19.00)
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)


    def test_create_educational_background(self):
        response = self.client.post(reverse('users:educationalbackgrounds_list'),
                                    data={'title': 'test', 'educationalInstitute': 'company',
                                          'major': 'test', 'grad': 'test', 'start': '2020-1-1',
                                          'adjusted': 19.00})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_educational_background(self):
        response = self.client.put(reverse('users:educationalbackground', args=(self.educationalBackground.pk,)),
                                   data={'title': 'test', 'educationalInstitute': 'company',
                                         'major': 'test', 'grad': 'test', 'start': '2020-1-1',
                                         'adjusted': 19.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_educational_background(self):
        response = self.client.get(reverse('users:educationalbackground', args=(self.educationalBackground.pk,)),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_educational_background(self):
        response = self.client.delete(reverse('users:educationalbackground', args=(self.educationalBackground.pk,)),)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_user_educational_backgrounds(self):
        response = self.client.get(reverse('users:educationalbackgrounds_list'),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NotificationTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.notification = Notification.objects.create(profile=self.user1, text='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_notifications(self):
        response = self.client.get(reverse('users:notification'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_as_read(self):
        response = self.client.get(reverse('users:notification_markasread', args=(self.notification.pk,)),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ApplyForJobTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.user2, self.tokenUser2 = UserToken('testman2')
        self.employee = Employee.objects.create(profile=self.user1, name='test')
        self.company = Company.objects.create(profile=self.user2, companyName='test')
        self.apply4job = ApplyForJob.objects.create(employee=self.employee, company=self.company, sender='c',
                                                    text='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_create_apply_for_job(self):
        response = self.client.post(reverse('users:applyforjobs_list'),
                                    data={'company': self.company.pk, 'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_apply_for_job(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser2)
        response = self.client.put(reverse('users:applyforjob', args=(self.apply4job.pk,)),
                                   data={'text': 'a'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_apply_for_job(self):
        response = self.client.get(reverse('users:applyforjob', args=(self.apply4job.pk,)),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reject_apply_for_job(self):
        response = self.client.post(reverse('users:reject_applyforjob', args=(self.apply4job.pk,)),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_apply_for_job(self):
        response = self.client.post(reverse('users:accept_applyforjob', args=(self.apply4job.pk,)),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_applies_for_job(self):
        response = self.client.get(reverse('users:applyforjobs_list', ),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class JobOfferTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.company = Company.objects.create(profile=self.user1, companyName='test')
        self.industry = Industry.objects.create(title='test')
        self.category = Category.objects.create(title='test', industry=self.industry)
        self.joboffer = JobOffer.objects.create(company=self.company, title='test', count=20, jobType='F')
        self.joboffer.category.add(self.category)
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_create_job_offer(self):
        response = self.client.post(reverse('users:joboffers_list'),
                                    data={'title': 'test', 'category': self.category.id,
                                          'count': 24, 'jobType': 'F'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_job_offer(self):
        response = self.client.get(reverse('users:joboffer', args=(self.joboffer.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_job_offers(self):
        response = self.client.get(reverse('users:joboffers_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_job_offer(self):
        response = self.client.delete(reverse('users:joboffer', args=(self.joboffer.pk,)), )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EmployeeTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.employee = Employee.objects.create(profile=self.user1, name='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_get_employees(self):
        response = self.client.get(reverse('users:employees'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_employee(self):
        response = self.client.get(reverse('users:employee', args=(self.employee.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_employee(self):
        response = self.client.put(reverse('users:employee', args=(self.employee.pk,)),
                                   data={'name': 'test', 'phoneNumber': '09304895880', 'gender': 'M',
                                         'relationshipStatus': 'S', 'jobSearchStatus': 'A'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CompanyTest(APITestCase):
    def setUp(self):
        self.user1, self.tokenUser1 = UserToken('testman1')
        self.company = Company.objects.create(profile=self.user1, companyName='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.tokenUser1)

    def test_get_companies(self):
        response = self.client.get(reverse('users:companies'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_company(self):
        response = self.client.get(reverse('users:company', args=(self.company.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_company(self):
        response = self.client.put(reverse('users:company', args=(self.company.pk,)),
                                   data={'companyName': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
