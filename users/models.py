import datetime

from django.db import models
from django.db.models.signals import pre_save

from Posts.utils import *


class Wallet(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    following = models.ManyToManyField(
        'Wallet', blank=True, related_name='followers')
    block = models.ManyToManyField(
        'Wallet', blank=True, related_name='blockBy')
    ban = models.BooleanField(default=False)
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class FollowRequest(models.Model):
    STATUS_CHOICES = [
        ('a', 'accepted'),
        ('w', "waiting"),
        ('r', 'rejected'),
    ]
    sender = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='followRequestSent')
    receiver = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='followRequests')
    status = models.CharField(choices=STATUS_CHOICES,
                              default='w', max_length=1)

    def __str__(self):
        return f'{self.sender} - {self.receiver}'


class Industries(models.Model):
    STATUS_CHOICES = [
        ('a', 'accepted'),
        ('w', "waiting"),
        ('r', 'rejected'),
    ]

    title = models.CharField(max_length=1024, unique=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              default='w', max_length=1)

    def __str__(self):
        return self.title


class Category(models.Model):
    STATUS_CHOICES = [
        ('a', 'accepted'),
        ('w', "waiting"),
        ('r', 'rejected'),
    ]

    industry = models.ForeignKey(
        Industries, null=True,  on_delete=models.CASCADE, related_name='category')
    title = models.CharField(max_length=500, unique=True)
    upperCategory = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name='reverseCategory')
    status = models.CharField(choices=STATUS_CHOICES,
                              default='w', max_length=1)

    def __str__(self):
        return self.title


class Tech(models.Model):
    title = models.CharField(max_length=1024, unique=True)
    industry = models.ForeignKey(
        Industries, blank=True, on_delete=models.CASCADE, related_name='tech')

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=1024, unique=True)
    industry = models.ForeignKey(
        Industries, blank=True, null=True, on_delete=models.CASCADE, related_name='role')

    def __str__(self):
        return self.title


class Company(models.Model):
    relatedName = 'company'

    STATUS_CHOICES = [
        ('a', 'accepted'),
        ('w', "waiting"),
        ('r', 'rejected'),
    ]

    profile = models.OneToOneField(
        "Wallet", on_delete=models.CASCADE, related_name=relatedName)
    profilePic = models.ImageField(upload_to=upload_profilePic, blank=True)
    companyName = models.CharField(max_length=2048)
    about = models.TextField(blank=True)
    workEmail = models.EmailField(blank=True)
    phoneNumber = models.CharField(max_length=15, blank=True)
    website = models.CharField(max_length=500, blank=True)
    foundedIn = models.DateField(blank=True, null=True)
    category = models.ManyToManyField(
        Category, blank=True, related_name=relatedName)
    industries = models.ManyToManyField(
        Industries, blank=True, related_name=relatedName)
    employeeCount = models.CharField(max_length=1024, blank=True)
    needEmployee = models.BooleanField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              default='w', max_length=1)

    def __str__(self):
        return self.profile.pk


class CompanyDocument(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='companyDocument')
    document = models.FileField(upload_to=upload_companyDocument)


class JobOffer(models.Model):
    relatedName = 'jobOffer'

    JOB_TYPE_CHOICES = (
        ('F', 'Full-time'),
        ('C', 'Contract'),
        ('I', 'Internship'),
        ('R', 'Remote'),
    )

    title = models.CharField(max_length=1024)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name=relatedName)
    job = models.ManyToManyField(Job, blank=True, related_name=relatedName)
    tech = models.ManyToManyField(Tech, blank=True, related_name=relatedName)
    category = models.ManyToManyField(Category, related_name=relatedName)
    count = models.PositiveIntegerField()
    jobType = models.CharField(max_length=1, choices=JOB_TYPE_CHOICES)
    salary = models.CharField(max_length=1024, blank=True)
    text = models.TextField(blank=True)


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

    profile = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, related_name=relatedName)
    name = models.CharField(max_length=1024)
    profilePic = models.ImageField(upload_to=upload_profilePic, blank=True)
    category = models.ManyToManyField(
        Category, blank=True, related_name=relatedName)
    about = models.TextField(blank=True)
    address = models.CharField(max_length=1024, blank=True)
    phoneNumber = models.CharField(max_length=13)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    relationshipStatus = models.CharField(
        choices=RELATIONSHIP_STATUS_CHOICES, max_length=1)
    jobSearchStatus = models.CharField(
        max_length=1, choices=JOB_SEARCH_STATUS_CHOICES)
    minimumAnnualSalary = models.PositiveIntegerField(blank=True, null=True)
    techWantsToWorkWith = models.ManyToManyField(
        Tech, blank=True, related_name='employeeProfileTechWantsToWorkWith')
    techWantsToNotWorkWith = models.ManyToManyField(Tech, blank=True,
                                                    related_name='employeeProfileTechWantsToNotWorkWith')
    role = models.ManyToManyField(Job, blank=True, related_name=relatedName)
    industries = models.ManyToManyField(
        Industries, blank=True, related_name='employeeProfileIndustries')
    industriesToExclude = models.ManyToManyField(Industries, blank=True,
                                                 related_name='employeeProfileIndustriesToExclude')
    jobType = models.CharField(
        max_length=1, choices=JOB_TYPE_CHOICES, blank=True)
    hire = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.profile.pk


class WorkExperience(models.Model):
    relatedName = 'workExperience'

    profile = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name=relatedName)
    title = models.CharField(max_length=1024)
    company = models.CharField(max_length=1024)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    stillWorking = models.BooleanField()
    tech = models.ManyToManyField(Tech, related_name=relatedName, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class EducationalBackground(models.Model):
    relatedName = 'educationalBackground'

    profile = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name=relatedName)
    grad = models.CharField(max_length=1024)
    major = models.CharField(max_length=1024)
    educationalInstitute = models.CharField(max_length=1024)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    stillStudying = models.BooleanField()
    adjusted = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.profile)


class Achievement(models.Model):
    relatedName = 'achievement'

    profile = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name=relatedName)
    title = models.CharField(max_length=1024)
    certificateProvider = models.CharField(max_length=1024)
    date = models.DateField()
    siteAddress = models.CharField(max_length=1024, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.profile.id)


class Notification(models.Model):
    profile = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='notification')
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

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name=relatedName)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name=relatedName)
    sender = models.CharField(max_length=1, choices=SENDER_CHOICES)
    text = models.TextField()
    status = models.CharField(
        default='w', choices=STATUS_CHOICES, max_length=1)
    non_cooperation = models.BooleanField(default=False)
    nonCooperationDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.employee}-{self.company}'


class ReportReason(models.Model):
    title = models.CharField(max_length=2048)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Report(models.Model):
    TYPE_CHOICE = (
        ('p', 'post'),
        ('c', 'comment'),
        ('q', 'question'),
        ('a', 'answer'),
        ('w', 'wallet')
    )

    type = models.CharField(max_length=1, choices=TYPE_CHOICE)
    # The slug is thing's thing you want to report
    slug = models.SlugField()
    reporter = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='report')
    reason = models.ForeignKey(
        ReportReason, on_delete=models.CASCADE, related_name='report')
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)


def FollowRequestPreSave(sender, instance, *args, **kwargs):
    notif = Notification(profile=instance.receiver,
                         text="You have a new follow request")
    notif.save()
    if instance.status == 'a':
        instance.sender.following.add(instance.receiver)


def EmployeePreSave(sender, instance, *args, **kwargs):
    if instance.profilePic == '':
        instance.profilePic = f'profiles/Default/{random.randint(1, 10)}.jpeg'


def CompanyPreSave(sender, instance, *args, **kwargs):
    if instance.profilePic == '':
        instance.profilePic = f'profiles/Default/{random.randint(1, 10)}.jpeg'


def ApplyForJobPreSave(sender, instance, *args, **kwargs):
    if instance.sender == 'e':
        Notif = Notification(profile=instance.company.profile,
                             text=f'{instance.employee.name} sent you request',
                             slug='a')
    else:
        Notif = Notification(profile=instance.employee.profile,
                             text=f'{instance.company.companyName} sent you request',
                             slug='')
    Notif.save()
    if instance.non_cooperation:
        instance.nonCooperationDate = datetime.datetime.now().date()


pre_save.connect(ApplyForJobPreSave, ApplyForJob)
pre_save.connect(EmployeePreSave, Employee)
pre_save.connect(CompanyPreSave, Company)
pre_save.connect(FollowRequestPreSave, FollowRequest)
