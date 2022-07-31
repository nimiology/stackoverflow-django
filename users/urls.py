from users.views import *
from django.urls import path

app_name = 'users'
urlpatterns = [
    path('wallet/<username>/', MyUserAPI.as_view(), name='wallet'),
    path('follow/<username>/', FollowAPI.as_view(), name='follow'),
    path('user/<slug>/following/', FollowingAPI.as_view(), name='followings'),
    path('user/<slug>/follower/', FollowersAPI.as_view(), name='followers'),

    path('industry/<title>/', IndustriesAPI.as_view(), name='industry'),
    path('industry/', GetAllIndustriesAPI.as_view(), name='industries_list'),

    path('category/<int:pk>/', CategoryAPI.as_view(), name='category'),
    path('category/', GetAllCategoryAPI.as_view(), name='categories_list'),

    path('tech/<int:pk>/', TechAPI.as_view(), name='tech'),
    path('tech/', GetAllTechAPI.as_view(), name='techs_list'),

    path('job/<int:pk>', JobAPI.as_view(), name='job'),
    path('jobs/', GetAllJobAPI.as_view(), name='jobs_list'),

    path('educationalbackground/<int:pk>/', EducationalBackgroundAPI.as_view(), name='educationalbackground'),
    path('educationalbackground/', EducationalBackgroundListAPI.as_view(), name='educationalbackgrounds_list'),

    path('workexperience/<int:pk>/', WorkExperienceAPI.as_view(), name='workexperience'),
    path('workexperience/', WorkExperienceListAPI.as_view(), name='workexperiences_list'),

    path('achievement/<int:pk>/', AchievementAPI.as_view(), name='achievement'),
    path('achievement/', AchievementLIstAPI.as_view(), name='achievements_list'),

    path('notification/', UserNotificationListAPI.as_view(), name='notification'),
    path('notification/<pk>/markasread/', NotificationMarkAsRead.as_view(), name='notification_markasread'),

    path('applyforjob/<int:pk>/', ApplyForJobAPI.as_view(), name='applyforjob'),
    path('applyforjob/<int:pk>/accept/', VerifyApplyForJobAPI.as_view(), name='accept_applyforjob'),
    path('applyforjob/<int:pk>/reject/', VerifyApplyForJobAPI.as_view(), name='reject_applyforjob'),
    path('applyforjob/', AppliesForJobListAPI.as_view(), name='applyforjobs_list'),

    path('joboffer/<int:pk>/', JobOfferAPI.as_view(), name='joboffer'),
    path('joboffer/', JobOfferListAPI.as_view(), name='joboffers_list'),

    path('company/', CompanyAll.as_view(), name='companies'),
    path('employee/', EmployeeAll.as_view(), name='employees'),
    path('company/<int:pk>/', CompanyRU.as_view(), name='company'),
    path('employee/<int:pk>/', EmployeeRU.as_view(), name='employee'),

]
