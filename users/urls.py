from users.views import *
from django.urls import path

urlpatterns = [
    path('reportreason', ReportReasonAPI.as_view()),
    path('reportreason/<int:pk>', ReportReasonAPI.as_view()),
    path('reportreasons', AllReportReasonsAPI.as_view()),

    path('report', ReportAPI.as_view()),
    path('reports', ReportsAPI.as_view()),
    path('report/<int:pk>', ReportAPI.as_view()),
]