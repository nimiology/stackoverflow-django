from django.conf.urls import url

from users.views import *
from django.urls import path, include

urlpatterns = [
    url('auth/', include('djoser.urls')),
    url('auth/', include('djoser.urls.jwt')),

    path('wallet/<pk>', WalletAPI.as_view()),
    path('follow/<slug>', FollowAPI.as_view()),
    path('user/<slug>/following', FollowingAPI.as_view()),
    path('user/<slug>/follower', FollowersAPI.as_view()),

    path('industry', IndustriesAPI.as_view()),
    path('industry/<int:pk>', IndustriesAPI.as_view()),
    path('industries', GetAllIndustriesAPI.as_view()),

    path('category', CategoryAPI.as_view()),
    path('category/<int:pk>', CategoryAPI.as_view()),
    path('categorys', GetAllCategoryAPI.as_view()),

    path('tech', TechAPI.as_view()),
    path('tech/<int:pk>', TechAPI.as_view()),
    path('techs', GetAllTechAPI.as_view()),

    path('job', JobAPI.as_view()),
    path('job/<int:pk>', JobAPI.as_view()),
    path('jobs', GetAllJobAPI.as_view()),

    path('companydocument', CompanyDocumentAPI.as_view()),
    path('companydocument/<int:pk>', CompanyDocumentAPI.as_view()),
    path('company/<slug>/companydocument', CompanyDocuments.as_view()),

    path('educationalbackground', EducationalBackgroundAPI.as_view()),
    path('educationalbackground/<int:pk>', EducationalBackgroundAPI.as_view()),
    path('user/<slug>/educationalbackground', ProfileEducationalBackground.as_view()),

    path('workexperience', WorkExperienceAPI.as_view()),
    path('workexperience/<int:pk>', WorkExperienceAPI.as_view()),
    path('user/<slug>/workexperience', ProfileWorkExperience.as_view()),

    path('achievement', AchievementAPI.as_view()),
    path('achievement/<int:pk>', AchievementAPI.as_view()),
    path('user/<slug>/achievement', ProfileAchievement.as_view()),

    path('notification', UserNotification.as_view()),
    path('notification/custom', CustomNotification.as_view()),
    path('notification/<id>/markasread', NotificationMarkAsRead.as_view()),

    path('applyforjob', ApplyForJobAPI.as_view()),
    path('applyforjob/<int:pk>', ApplyForJobAPI.as_view()),
    path('applyforjob/<int:pk>/accept', VerifyApplyForJobAPI.as_view()),
    path('applyforjob/<int:pk>/reject', VerifyApplyForJobAPI.as_view()),
    path('user/<slug>/applyforjob', AllAppliesForJob.as_view()),

    path('joboffer', JobOfferAPI.as_view()),
    path('joboffer/<int:pk>', JobOfferAPI.as_view()),
    path('company/<slug>/joboffers', GetAllProfileJobOffer.as_view()),
    path('joboffers', SearchJobOffers.as_view()),


    path('company/', CompanyAll.as_view()),
    path('employee/', EmployeeAll.as_view()),


]
