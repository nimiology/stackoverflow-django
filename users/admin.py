from django.contrib import admin

from .models import *


# Register your models here.

class ApplyForJobAdmin(admin.ModelAdmin):
    list_display = ['employee', 'company', 'sender', 'status']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("profile", "companyName", "workEmail", "phoneNumber")
    search_fields = ("companyName", "workEmail")
    ordering = ['companyName', "profile"]


class CategoryProfileAdmin(admin.ModelAdmin):
    list_display = ("title", "upperCategory")


class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("profile", "title", "company")
    search_fields = ("title", "company", 'profile')
    ordering = ['profile', 'company']


class EducationalBackgroundAdmin(admin.ModelAdmin):
    list_display = ("profile", "grad", "major", 'educationalInstitute')
    search_fields = ("profile", "major", 'educationalInstitute')
    ordering = ['profile', 'grad']


class AchievementAdmin(admin.ModelAdmin):
    list_display = ("profile", "title", "certificateProvider", 'date')
    list_filter = ("profile", 'date')
    search_fields = ("title", "certificateProvider", 'profile')
    ordering = ['profile', 'title']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("profile", "date", 'text', "markAsRead")


admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee)
admin.site.register(Wallet)
admin.site.register(Category, CategoryProfileAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(EducationalBackground, EducationalBackgroundAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Industries)
admin.site.register(Tech)
admin.site.register(Job)
admin.site.register(JobOffer)
admin.site.register(ApplyForJob, ApplyForJobAdmin)
admin.site.register(CompanyDocument)
admin.site.register(ReportReason)
admin.site.register(Report)
admin.site.register(FollowRequest)
