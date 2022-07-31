from users.views import *
from django.urls import path, include

app_name = 'users'
urlpatterns = [
    path('wallet/<username>', MyUserAPI.as_view(), name='wallet'),
    path('follow/<slug>', FollowAPI.as_view(), name='follow'),
    path('user/<slug>/following', FollowingAPI.as_view(), name='followings'),
    path('user/<slug>/follower', FollowersAPI.as_view(), name='followers'),

    path('industry', IndustriesAPI.as_view(), name='create_industry'),
    path('industry/<int:pk>', IndustriesAPI.as_view(), name='industry'),
    path('industries', GetAllIndustriesAPI.as_view(), name='industries'),

    path('category', CategoryAPI.as_view(), name='create_category'),
    path('category/<int:pk>', CategoryAPI.as_view(), name='category'),
    path('categorys', GetAllCategoryAPI.as_view(), name='categories'),

    path('tech', TechAPI.as_view(), name='create_tech'),
    path('tech/<int:pk>', TechAPI.as_view(), name='tech'),
    path('techs', GetAllTechAPI.as_view(), name='techs'),

    path('job', JobAPI.as_view(), name='create_job'),
    path('job/<int:pk>', JobAPI.as_view(), name='job'),
    path('jobs', GetAllJobAPI.as_view(), name='jobs'),

    path('educationalbackground', EducationalBackgroundAPI.as_view(), name='create_educationalbackground'),
    path('educationalbackground/<int:pk>', EducationalBackgroundAPI.as_view(), name='educationalbackground'),
    path('user/<slug>/educationalbackground', ProfileEducationalBackground.as_view(), name='user_educationalbackgrounds'),

    path('workexperience', WorkExperienceAPI.as_view(), name='create_workexperience'),
    path('workexperience/<int:pk>', WorkExperienceAPI.as_view(), name='workexperience'),
    path('user/<slug>/workexperience', ProfileWorkExperience.as_view(), name='user_workexperiences'),

    path('achievement', AchievementAPI.as_view(), name='create_achievement'),
    path('achievement/<int:pk>', AchievementAPI.as_view(), name='achievement'),
    path('user/<slug>/achievement', ProfileAchievement.as_view(), name='user_achievements'),

    path('notification', UserNotification.as_view(), name='notification'),
    path('notification/<id>/markasread', NotificationMarkAsRead.as_view(), name='notification_markasread'),

    path('applyforjob', ApplyForJobAPI.as_view(), name='create_applyforjob'),
    path('applyforjob/<int:pk>', ApplyForJobAPI.as_view(), name='applyforjob'),
    path('applyforjob/<int:pk>/accept', VerifyApplyForJobAPI.as_view(), name='accept_applyforjob'),
    path('applyforjob/<int:pk>/reject', VerifyApplyForJobAPI.as_view(), name='reject_applyforjob'),
    path('user/<slug>/applyforjob', AllAppliesForJob.as_view(), name='user_applyforjob'),

    path('joboffer', JobOfferAPI.as_view(), name='create_joboffer'),
    path('joboffer/<int:pk>', JobOfferAPI.as_view(), name='joboffer'),
    path('company/<slug>/joboffers', GetAllProfileJobOffer.as_view(), name='company_joboffers'),
    path('joboffers', SearchJobOffers.as_view(), name='joboffers'),


    path('company/', CompanyAll.as_view(), name='companies'),
    path('employee/', EmployeeAll.as_view(), name='employees'),
    path('company/<int:pk>/', CompanyRU.as_view(), name='company'),
    path('employee/<int:pk>/', EmployeeRU.as_view(), name='employee'),

]
