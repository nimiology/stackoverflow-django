import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save

from config import settings
from posts.utils import *


class MyUser(AbstractUser):
    following = models.ManyToManyField('self', blank=True)
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Industry(models.Model):
    title = models.CharField(max_length=1024, primary_key=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    industry = models.ForeignKey(Industry, null=True, on_delete=models.CASCADE, related_name='category')
    title = models.CharField(max_length=500, unique=True)
    upperCategory = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name='reverseCategory')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Tech(models.Model):
    title = models.CharField(max_length=1024, unique=True, null=True, blank=True)
    industry = models.ForeignKey(Industry, null=True, blank=True, on_delete=models.CASCADE, related_name='tech')

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=1024, unique=True)
    industry = models.ForeignKey(Industry, blank=True, null=True, on_delete=models.CASCADE, related_name='role')

    def __str__(self):
        return self.title


class Company(models.Model):
    relatedName = 'company'

    profile = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name=relatedName)
    profilePic = models.ImageField(upload_to=upload_profilePic, blank=True)
    companyName = models.CharField(max_length=2048)
    about = models.TextField(blank=True)
    workEmail = models.EmailField(blank=True)
    phoneNumber = models.CharField(max_length=15, blank=True)
    website = models.CharField(max_length=500, blank=True)
    foundedIn = models.DateField(blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True, related_name=relatedName)
    industries = models.ManyToManyField(Industry, blank=True, related_name=relatedName)
    employeeCount = models.CharField(max_length=1024, blank=True)
    needEmployee = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.profile


class JobOffer(models.Model):
    relatedName = 'jobOffer'

    JOB_TYPE_CHOICES = (
        ('F', 'Full-time'),
        ('C', 'Contract'),
        ('I', 'Internship'),
        ('R', 'Remote'),
    )

    title = models.CharField(max_length=1024)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name=relatedName)
    job = models.ManyToManyField(Job, blank=True, related_name=relatedName)
    tech = models.ManyToManyField(Tech, blank=True, related_name=relatedName)
    category = models.ManyToManyField(Category, related_name=relatedName)
    count = models.PositiveIntegerField()
    jobType = models.CharField(max_length=1, choices=JOB_TYPE_CHOICES)
    salary = models.CharField(max_length=1024, blank=True)
    text = models.TextField(blank=True)
    seo = models.JSONField(blank=True, null=True)


class Employee(models.Model):
    relatedName = 'employee'

    JOB_SEARCH_STATUS_CHOICES = (
        ('A', 'Actively looking right now'),
        ('O', 'Open, but not actively looking'),
        ('N', 'Not interested in jobs')
    )
    JOB_TYPE_CHOICES = (
        ('F', 'Full-time'),
        ('C', 'Contract'),
        ('I', 'Internship')
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('D', "Don't wanna say")
    )
    RELATIONSHIP_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married')
    )

    profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=relatedName)
    name = models.CharField(max_length=1024)
    profilePic = models.ImageField(upload_to=upload_profilePic, blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name=relatedName)
    about = models.TextField(blank=True)
    address = models.CharField(max_length=1024, blank=True)
    phoneNumber = models.CharField(max_length=13)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    relationshipStatus = models.CharField(choices=RELATIONSHIP_STATUS_CHOICES, max_length=1)
    jobSearchStatus = models.CharField(max_length=1, choices=JOB_SEARCH_STATUS_CHOICES)
    minimumAnnualSalary = models.PositiveIntegerField(blank=True, null=True)
    techWantsToWorkWith = models.ManyToManyField(Tech, blank=True, related_name='employeeProfileTechWantsToWorkWith')
    techWantsToNotWorkWith = models.ManyToManyField(Tech, blank=True,
                                                    related_name='employeeProfileTechWantsToNotWorkWith')
    role = models.ManyToManyField(Job, blank=True, related_name=relatedName)
    industries = models.ManyToManyField(Industry, blank=True, related_name='employeeProfileIndustries')
    industriesToExclude = models.ManyToManyField(Industry, blank=True,
                                                 related_name='employeeProfileIndustriesToExclude')
    jobType = models.CharField(max_length=1, choices=JOB_TYPE_CHOICES, blank=True)
    hire = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.profile


class WorkExperience(models.Model):
    relatedName = 'workExperience'

    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=relatedName)
    title = models.CharField(max_length=1024)
    company = models.CharField(max_length=1024)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    tech = models.ManyToManyField(Tech, related_name=relatedName, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class EducationalBackground(models.Model):
    relatedName = 'educationalBackground'

    profile = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name=relatedName)
    grad = models.CharField(max_length=1024)
    major = models.CharField(max_length=1024)
    educationalInstitute = models.CharField(max_length=1024)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    adjusted = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.profile)


class Achievement(models.Model):
    relatedName = 'achievement'

    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=relatedName)
    title = models.CharField(max_length=1024)
    certificateProvider = models.CharField(max_length=1024)
    date = models.DateField()
    siteAddress = models.URLField(max_length=1024, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.profile


class Notification(models.Model):
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification')
    text = models.TextField()
    slug = models.SlugField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    markAsRead = models.BooleanField(default=False)

    def __str__(self):
        return str(self.profile)


class ApplyForJob(models.Model):
    relatedName = 'applyForJob'

    SENDER_CHOICES = (
        ('e', 'employee'),
        ('c', 'company')
    )

    STATUS_CHOICES = (
        ('w', 'waiting'),
        ('a', 'accepted'),
        ('r', 'rejected')
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name=relatedName)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name=relatedName)
    sender = models.CharField(max_length=1, choices=SENDER_CHOICES)
    text = models.TextField()
    status = models.CharField(default='w', choices=STATUS_CHOICES, max_length=1)
    nonCooperation = models.BooleanField(default=False)
    nonCooperationDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.employee}-{self.company}'


def ApplyForJobPreSave(sender, instance, *args, **kwargs):
    if instance.sender == 'e':
        notification = Notification(profile=instance.company.profile,
                                    text=f'{instance.employee.name} sent you request',
                                    slug='a')
    else:
        notification = Notification(profile=instance.employee.profile,
                                    text=f'{instance.company.companyName} sent you request',
                                    slug='')
    notification.save()
    if instance.nonCooperation:
        instance.nonCooperationDate = datetime.datetime.now().date()


pre_save.connect(ApplyForJobPreSave, ApplyForJob)
