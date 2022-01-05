from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from Posts.permission import IsAdmin, IsItOwner
from users.permission import IsItOwnerCompany
from users.serializer import *
from users.utils import GetWallet, FindWallet, GetCompany


class WalletAPI(GenericAPIView, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = WalletSerializer
    queryset = UserInfo.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Wallet"""
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """delete wallet profile by admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.destroy(request, *args, **kwargs)


class FollowAPI(APIView):
    def post(self, request, *args, **kwargs):
        """Follow"""
        profile = GetWallet(request)
        authID = kwargs['slug']
        following = FindWallet(authID)
        if following != profile:
            profile.following.add(following)
            notif = Notification(profile=following,
                                 text=f'{profile.id} followed you!', )
            notif.save()
            return Response(data=WalletSerializer(following).data, status=status.HTTP_200_OK)
        else:
            raise ValidationError('You cant follow yourself')


class FollowingAPI(ListAPIView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        """Get User Following"""
        authID = self.kwargs['slug']
        profile = FindWallet(authID)
        followings = profile.following.all()
        return followings


class FollowersAPI(ListAPIView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        """Get User Following"""
        authID = self.kwargs['slug']
        profile = FindWallet(authID)
        followings = profile.followers.all()
        return followings


class IndustriesAPI(GenericAPIView, CreateModelMixin,
                    RetrieveModelMixin, UpdateModelMixin,
                    DestroyModelMixin):
    serializer_class = IndustriesSerializer
    queryset = Industries.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Industry"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Industry"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Industry By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Industry By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        GetWallet(self.request)
        return serializer.save()


class GetAllIndustriesAPI(ListAPIView):
    """Get All Industries"""
    serializer_class = IndustriesSerializer
    # search fields
    filterset_fields = ['title', 'status']
    queryset = Industries.objects.all()


class CategoryAPI(GenericAPIView, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Category """
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Category """
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Category By Admin"""
        self.serializer_class = VerifyCategorySerializer
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Category By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        GetWallet(self.request)
        return serializer.save(status='w')


class GetAllCategoryAPI(ListAPIView):
    """Get All Categories"""
    serializer_class = CategorySerializer
    filterset_fields = ['title', 'industry__title', 'upperCategory__title', 'status']
    queryset = Category.objects.all()


class TechAPI(GenericAPIView, CreateModelMixin,
              RetrieveModelMixin, UpdateModelMixin,
              DestroyModelMixin):
    serializer_class = TechSerializer
    queryset = Tech.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Tech """
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Tech """
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Tech By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Tech By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        GetWallet(self.request)
        return serializer.save()


class GetAllTechAPI(ListAPIView):
    """Get All Techs"""
    serializer_class = TechSerializer
    filterset_fields = ['title', 'industry__title']
    queryset = Tech.objects.all()


class JobAPI(GenericAPIView, CreateModelMixin,
             RetrieveModelMixin, UpdateModelMixin,
             DestroyModelMixin):
    serializer_class = JobSerializer
    queryset = Job.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Job """
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Job"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Job By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Job By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        GetWallet(self.request)
        return serializer.save()


class GetAllJobAPI(ListAPIView):
    """Get All Jobs"""
    serializer_class = JobSerializer
    filterset_fields = ['title', 'industry__title']
    queryset = Job.objects.all()


class CompanyDocumentAPI(GenericAPIView, CreateModelMixin,
                         RetrieveModelMixin, UpdateModelMixin,
                         DestroyModelMixin):
    serializer_class = CompanyDocumentSerializer
    queryset = CompanyDocument.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Company Document"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Company Document"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Company Document"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Company Document"""
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        wallet = GetWallet(self.request)
        try:
            company = wallet.company
            company.status = 'w'
            company.save()
            return serializer.save(company=company)
        except Company.DoesNotExist:
            raise ValidationError('There is no Company on this wallet')

    def perform_update(self, serializer):
        wallet = GetWallet(self.request)
        try:
            company = wallet.company
            instance = get_object_or_404(CompanyDocument, pk=self.kwargs['pk'])
            """Is he him?"""
            if company == instance.company:
                company = wallet.company
                company.status = 'w'
                company.save()
                return instance.delete()
            else:
                raise ValidationError('access denied!')
        except Company.DoesNotExist:
            raise ValidationError('There is no Company on this wallet')

    def perform_destroy(self, instance):
        wallet = GetWallet(self.request)
        try:
            company = wallet.company
            """Is he him?"""
            if company == instance.company:
                company = wallet.company
                company.status = 'w'
                company.save()
                return instance.delete()
            else:
                raise ValidationError('access denied!')
        except Company.DoesNotExist:
            raise ValidationError('There is no Company on this wallet')


class CompanyDocuments(ListAPIView):
    serializer_class = CompanyDocumentSerializer

    def get_queryset(self):
        """Get Company's Document"""
        username = self.kwargs['slug']
        company = get_object_or_404(Company, profile__username=username)
        companyDocuments = company.companyDocument.all()
        return companyDocuments


class EducationalBackgroundAPI(GenericAPIView, CreateModelMixin,
                               RetrieveModelMixin, UpdateModelMixin,
                               DestroyModelMixin):
    serializer_class = EducationalBackgroundSerializer
    queryset = EducationalBackground.objects.all()

    def get(self, request, *args, **kwargs):
        """Get EducationalBackground"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create EducationalBackground"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit EducationalBackground"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete EducationalBackground"""
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set Profile"""
        try:
            employee = GetWallet(self.request).employee
            return serializer.save(profile=employee)
        except Employee.DoesNotExist:
            raise ValidationError('There is no employee on this profile')

    def perform_update(self, serializer):
        """Set Profile"""
        try:
            employee = GetWallet(self.request).employee
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
            employee = GetWallet(self.request).employee
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


class WorkExperienceAPI(GenericAPIView, CreateModelMixin,
                        RetrieveModelMixin, UpdateModelMixin,
                        DestroyModelMixin):
    serializer_class = WorkExperienceSerializer
    queryset = WorkExperience.objects.all()

    def get(self, request, *args, **kwargs):
        """Get WorkExperience"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create WorkExperience"""
        return self.create(request, *args, **kwargs)

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
        return serializer.save(profile=GetWallet(self.request))

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


class AchievementAPI(GenericAPIView, CreateModelMixin,
                     RetrieveModelMixin, UpdateModelMixin,
                     DestroyModelMixin):
    serializer_class = AchievementSerializer
    queryset = Achievement.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Achievement"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Achievement"""
        return self.create(request, *args, **kwargs)

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
        return serializer.save(profile=GetWallet(self.request))

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


class CustomNotification(GenericAPIView, CreateModelMixin):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        """Custom notification by admin"""
        return self.create(request, *args, **kwargs)


class NotificationMarkAsRead(APIView):
    def post(self, request, *args, **kwargs):
        """Mark Notification as Read"""
        profile = GetWallet(request)
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
        profile = GetWallet(self.request)
        notifications = profile.notification.all().order_by('-date')
        return notifications


class ApplyForJobAPI(GenericAPIView, CreateModelMixin,
                     RetrieveModelMixin, UpdateModelMixin):
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
        profile = GetWallet(self.request)
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
        profile = GetWallet(self.request)
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
        profile = GetWallet(request)
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


class JobOfferAPI(GenericAPIView, CreateModelMixin,
                  RetrieveModelMixin, DestroyModelMixin,
                  UpdateModelMixin):
    serializer_class = JobOfferSerializer
    queryset = JobOffer.objects.all()

    def post(self, request, *args, **kwargs):
        """Create Job Offer"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Job Offer"""
        self.permission_classes = [IsItOwnerCompany]
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Get Job Offer"""
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Job Offer"""
        self.permission_classes = [IsItOwnerCompany]
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set Company on instance"""
        profile = GetWallet(self.request)
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
