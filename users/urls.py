from users.views import *
from django.urls import path

urlpatterns = [
    path('wallet/<pk>', WalletAPI.as_view()),
    path('block/<slug>', Block.as_view()),
    path('follow/<slug>', FollowAPI.as_view()),
    path('followrequests', FollowRequests.as_view()),
    path('followrequest/<id>/accept', AcceptFollowRequest.as_view()),
    path('followrequest/<id>/reject', RejectFollowRequest.as_view()),

    path('industry', IndustriesAPI.as_view()),
    path('industry/<int:pk>', IndustriesAPI.as_view()),
    path('industries', GetAllIndustriesAPI.as_view()),

    path('category', CategoryAPI.as_view()),
    path('category/<int:pk>', CategoryAPI.as_view()),
    path('categorys', GetAllCategoryAPI.as_view()),

    path('tech', TechAPI.as_view()),
    path('tech/<int:pk>', TechAPI.as_view()),
    path('techs', GetAllTechAPI.as_view()),

    path('reportreason', ReportReasonAPI.as_view()),
    path('reportreason/<int:pk>', ReportReasonAPI.as_view()),
    path('reportreasons', AllReportReasonsAPI.as_view()),

    path('report', ReportAPI.as_view()),
    path('reports', ReportsAPI.as_view()),
    path('report/<int:pk>', ReportAPI.as_view()),

]