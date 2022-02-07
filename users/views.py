from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView

from posts.permission import IsItOwner
from users.permission import IsItOwnerCompany, ReadOnly
from users.serializer import *
from users.utils import GetCompany


class MyUserAPI(RetrieveAPIView):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        """Get Wallet"""
        return self.retrieve(request, *args, **kwargs)


class FollowAPI(APIView):
    def post(self, request, *args, **kwargs):
        """Follow"""
        profile = request.user
        username = kwargs['slug']
        following = get_object_or_404(MyUser, username=username)
        if following != profile:
            profile.following.add(following)
            notif = Notification(profile=following,
                                 text=f'{profile.id} followed you!', )
            notif.save()
            return Response(data=MyUserSerializer(following).data, status=status.HTTP_200_OK)
        else:
            raise ValidationError('You cant follow yourself')


class FollowingAPI(ListAPIView):
    serializer_class = MyUserSerializer

    def get_queryset(self):
        """Get User Following"""
        username = self.kwargs['slug']
        profile = get_object_or_404(MyUser, username=username)
        followings = profile.following.all()
        return followings


class FollowersAPI(ListAPIView):
    serializer_class = MyUserSerializer

    def get_queryset(self):
        """Get User Followers"""
        username = self.kwargs['slug']
        profile = get_object_or_404(MyUser, username=username)
        followings = MyUser.objects.filter(following__in=[profile])
        return followings


class IndustriesAPI(CreateAPIView, RetrieveAPIView, DestroyAPIView):
    serializer_class = IndustriesSerializer
    queryset = Industries.objects.all()


class GetAllIndustriesAPI(ListAPIView):
    """Get All Industries"""
    serializer_class = IndustriesSerializer
    # search fields
    filterset_fields = ['title']
    queryset = Industries.objects.all()


class CategoryAPI(CreateAPIView, RetrieveAPIView, DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GetAllCategoryAPI(ListAPIView):
    """Get All Categories"""
    serializer_class = CategorySerializer
    filterset_fields = ['title', 'industry__title', 'upperCategory__title']
    queryset = Category.objects.all()


class TechAPI(CreateAPIView, RetrieveAPIView, DestroyAPIView):
    serializer_class = TechSerializer
    queryset = Tech.objects.all()


class GetAllTechAPI(ListAPIView):
    """Get All Techs"""
    serializer_class = TechSerializer
    filterset_fields = ['title', 'industry__title']
    queryset = Tech.objects.all()


class JobAPI(CreateAPIView, RetrieveAPIView, DestroyAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()


class GetAllJobAPI(ListAPIView):
    """Get All Jobs"""
    serializer_class = JobSerializer
    filterset_fields = ['title', 'industry__title']
    queryset = Job.objects.all()


class EducationalBackgroundAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = EducationalBackgroundSerializer
    queryset = EducationalBackground.objects.all()

    def put(self, request, *args, **kwargs):
        """Edit EducationalBackground"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete EducationalBackground"""
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set Profile"""
        try:
            employee = self.request.user.employee
            return serializer.save(profile=employee)
        except Employee.DoesNotExist:
            raise ValidationError('There is no employee on this profile')

    def perform_update(self, serializer):
        """Set Profile"""
        try:
            employee = self.request.user.employee
            education = get_object_or_404(EducationalBackground, id=self.kwargs['pk'])
            if employee == education.profile:
                return serializer.save(profile=employee)
            else:
                raise ValidationError('access denied!')
        except Employee.DoesNotExist:
            raise ValidationError('There is no employee on this profile')

    def perform_destroy(self, instance):
        education = get_object_or_404(EducationalBackground, id=self.kwargs['pk'])
        try:
            employee = self.request.user.employee
        except Employee.DoesNotExist:
            raise ValidationError('There is no employee on this profile')
        if employee == education.profile:
            return instance.delete()
        else:
            raise ValidationError('access denied!')


class ProfileEducationalBackground(ListAPIView):
    serializer_class = EducationalBackgroundSerializer

    def get_queryset(self):
        """Get profile's EducationalBackground"""
        username = self.kwargs['slug']
        employee = get_object_or_404(Employee, profile__username=username)
        education = employee.educationalBackground.all()
        return education


class WorkExperienceAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = WorkExperienceSerializer
    queryset = WorkExperience.objects.all()

    def put(self, request, *args, **kwargs):
        """Edit WorkExperience"""
        self.permission_classes = [IsItOwner]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete WorkExperience"""
        self.permission_classes = [IsItOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set Profile"""
        return serializer.save(profile=self.request.user)

    def perform_update(self, serializer):
        """Set Profile"""
        workExperience = get_object_or_404(WorkExperience, id=self.kwargs['pk'])
        self.check_object_permissions(request=self.request, obj=workExperience)
        return serializer.save(profile=workExperience.profile)

    def perform_destroy(self, instance):
        self.check_object_permissions(request=self.request, obj=instance)
        return instance.delete


class ProfileWorkExperience(ListAPIView):
    serializer_class = WorkExperienceSerializer

    def get_queryset(self):
        """Get profile's WorkExperience"""
        username = self.kwargs['slug']
        return WorkExperience.objects.filter(profile__username=username)


class AchievementAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = AchievementSerializer
    queryset = Achievement.objects.all()

    def put(self, request, *args, **kwargs):
        """Edit Achievement"""
        self.permission_classes = [IsItOwner]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Achievement"""
        self.permission_classes = [IsItOwner]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set Profile"""
        return serializer.save(profile=self.request.user)

    def perform_update(self, serializer):
        """Set Profile"""
        achievement = get_object_or_404(Achievement, id=self.kwargs['pk'])
        self.check_object_permissions(request=self.request, obj=achievement)
        return serializer.save(profile=achievement.profile)

    def perform_destroy(self, instance):
        self.check_object_permissions(request=self.request, obj=instance)
        return instance.delete


class ProfileAchievement(ListAPIView):
    serializer_class = AchievementSerializer

    def get_queryset(self):
        """Get profile's Achievment"""
        username = self.kwargs['slug']
        return Achievement.objects.filter(profile__username=username)


class NotificationMarkAsRead(APIView):
    def post(self, request, *args, **kwargs):
        """Mark Notification as Read"""
        profile = request.user
        notification = get_object_or_404(Notification, id=kwargs['id'])
        if notification.profile == profile:
            notification.markAsRead = True
            notification.save()
            serializer = NotificationSerializer(notification).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            raise ValidationError('access denied!')


class UserNotification(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """Get User's Notifications"""
        profile = self.request.user
        notifications = profile.notification.all().order_by('-date')
        return notifications


class ApplyForJobAPI(CreateAPIView, UpdateAPIView, RetrieveAPIView):
    serializer_class = ApplyForJobSerializer
    queryset = ApplyForJob.objects.all()

    def post(self, request, *args, **kwargs):
        """Apply For Job"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Apply For Job"""
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Get Apply For Job"""
        return self.retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        profile = self.request.user
        try:
            company = profile.company
            return serializer.save(company=company, sender='c', status='w')
        except Company.DoesNotExist:
            try:
                employee = profile.employee
                return serializer.save(employee=employee, sender='e', status='w')
            except Employee.DoesNotExist:
                raise ValidationError('There is no employee or company on this token!')

    def perform_update(self, serializer):
        profile = self.request.user
        instance = get_object_or_404(ApplyForJob, id=self.kwargs['pk'])
        if instance.status == 'w':
            if instance.sender == 'c':
                editor = instance.company.profile
            else:
                editor = instance.employee.profile
            if editor == profile:
                return serializer.save(company=instance.company, employee=instance.employee,
                                       sender=instance.sender, status=instance.status)
            else:
                raise ValidationError('access denied!')
        else:
            raise ValidationError("you've verified it before")


class AllAppliesForJob(ListAPIView):
    serializer_class = ApplyForJobSerializer

    def get_queryset(self):
        """Get profile's Job Offer"""
        username = self.kwargs['slug']
        if 'status' in self.request.data:
            if self.request.data['status'] in ['w', 'r', 'a']:
                qs = ApplyForJob.objects.filter(
                    Q(company__profile__username=username) | Q(employee__profile__username=username),
                    status=self.request.data['status'])
            else:
                qs = ApplyForJob.objects.filter(
                    Q(company__profile__username=username) | Q(employee__profile__username=username))
        else:
            qs = ApplyForJob.objects.filter(
                Q(company__profile__username=username) | Q(employee__profile__username=username))
        return qs


class VerifyApplyForJobAPI(APIView):
    def post(self, request, *args, **kwargs):
        """Verify apply"""
        id = kwargs['pk']
        profile = request.user
        apply = get_object_or_404(ApplyForJob, id=id)
        if apply.status == 'w':
            if apply.sender == 'c':
                verifier = apply.employee.profile
            else:
                verifier = apply.company.profile
            if verifier == profile:
                if 'accept' in request.get_full_path():
                    apply.status = 'a'
                elif 'reject' in request.get_full_path():
                    apply.status = 'r'
                else:
                    raise Http404

                apply.save()
                statusResponse = status.HTTP_200_OK
                data = ApplyForJobSerializer(apply).data
            else:
                raise ValidationError('access denied!')
        else:
            raise ValidationError("you've verified it before")

        return Response(data=data, status=statusResponse)


class JobOfferAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = JobOfferSerializer
    queryset = JobOffer.objects.all()

    def put(self, request, *args, **kwargs):
        """Edit Job Offer"""
        self.permission_classes = [IsItOwnerCompany]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Job Offer"""
        self.permission_classes = [IsItOwnerCompany]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set Company on instance"""
        profile = self.request.user
        company = GetCompany(profile)
        return serializer.save(company=company)

    def perform_update(self, serializer):
        instance = get_object_or_404(JobOffer, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, instance)
        return serializer.save(company=instance.company)

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        return instance.delete()


class GetAllProfileJobOffer(ListAPIView):
    serializer_class = JobOfferSerializer

    def get_queryset(self):
        """get profile job offer"""
        return JobOffer.objects.filter(company__profile__username=self.kwargs['slug'])


class SearchJobOffers(ListAPIView):
    serializer_class = JobOfferSerializer
    queryset = JobOffer.objects.all().order_by('-id')
    filterset_fields = ['title', 'job', 'tech', 'category', 'count', 'jobType', 'text']


class CompanyAll(ListAPIView):
    serializer_class = CompanyProfileSerializer
    queryset = Company.objects.all().order_by('-id')
    filterset_fields = ['companyName', 'about', 'foundedIn', 'employeeCount', 'industries', 'category', 'needEmployee']


class EmployeeAll(ListAPIView):
    serializer_class = EmployeeSerializer
    filterset_fields = ['gender', 'category', 'industries',
                        'relationshipStatus', 'jobSearchStatus']
    queryset = Employee.objects.all()


class EmployeeRU(RetrieveAPIView, UpdateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsItOwner | ReadOnly]
    queryset = Employee.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CompanyRU(RetrieveAPIView, UpdateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsItOwner | ReadOnly]
    queryset = Company.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
