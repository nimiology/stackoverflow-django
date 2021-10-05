from django.db.models import Q
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.views import APIView

from Posts.permission import IsAdmin, IsItOwner
from authentication.permission import OwnerOrReadOnly
from users.permission import IsItOwnerCompany
from users.serializer import *
from users.utils import GetWallet, FindWallet, GetCompany


class WalletAPI(GenericAPIView, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Wallet"""
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """delete wallet profile by admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.destroy(request, *args, **kwargs)


class Block(APIView):
    def post(self, request, *args, **kwargs):
        """Block"""
        profile1 = GetWallet(request)
        authID = kwargs['slug']
        profile2 = FindWallet(authID)
        if profile2 != profile1:
            if profile2 not in profile1.block.all():
                profile1.block.add(profile2)
            else:
                profile1.block.remove(profile2)
            return Response(data=WalletSerializer(profile1).data, status=status.HTTP_200_OK)
        else:
            raise ValidationError('You cant block yourself')


class AcceptFollowRequest(APIView):
    def post(self, request, *args, **kwargs):
        """Confirm Follow Request"""
        followRequest = get_object_or_404(FollowRequest, id=kwargs['id'])
        wallet = GetWallet(request)
        if followRequest.receiver == wallet:
            if followRequest.status == 'w':
                serializer = FollowRequestSerializer(followRequest)
                followRequest.status = 'a'
                followRequest.save()
                data = serializer.data
                statusResponse = status.HTTP_200_OK
            else:
                raise ValidationError('Previously reviewed!')
        else:
            raise ValidationError('access denied!')

        return Response(data=data, status=statusResponse)


class RejectFollowRequest(APIView):
    def post(self, request, *args, **kwargs):
        """Reject Follow Request"""
        followRequest = get_object_or_404(FollowRequest, id=kwargs['id'])
        wallet = GetWallet(request)
        if followRequest.receiver == wallet:
            if followRequest.status == 'w':
                serializer = FollowRequestSerializer(followRequest)
                followRequest.status = 'r'
                followRequest.save()
                data = serializer.data
                statusResponse = status.HTTP_200_OK
            else:
                raise ValidationError('Previously reviewed!')
        else:
            raise ValidationError('access denied!')

        return Response(data=data, status=statusResponse)


class FollowRequests(ListAPIView):
    serializer_class = FollowRequestSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        """Get All Follow Requests"""
        wallet = GetWallet(self.request)
        qs = wallet.followRequests.all()
        return qs


class FollowAPI(APIView):
    def post(self, request, *args, **kwargs):
        """Follow"""
        profile = GetWallet(request)
        authID = kwargs['slug']
        following = FindWallet(authID)
        if following != profile:
            if not following.private:
                profile.following.add(following)
                notif = Notification(profile=following,
                                     text=f'{profile.authID} followed you!', )
                notif.save()
                return Response(data=WalletSerializer(following).data, status=status.HTTP_200_OK)
            else:
                followRequest = FollowRequest(sender=profile, receiver=following)
                followRequest.save()
                return Response(data=FollowRequestSerializer(followRequest).data, status=status.HTTP_200_OK)
        else:
            raise ValidationError('You cant follow yourself')


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
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Industry By Admin"""
        self.serializer_class = VerifyIndustriesSerializer
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
        return serializer.save(status='w')


class GetAllIndustriesAPI(ListAPIView):
    """Get All Industries"""
    serializer_class = IndustriesSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
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
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    # search fields
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
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    # Search Fields
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
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    # Search Fields
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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get Company's Document"""
        id = self.kwargs['slug']
        company = get_object_or_404(Company, profile__id=id)
        companyDocuments = company.companyDocument.all()
        return companyDocuments


class VerifyCompany(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        """Verify Company"""
        company = get_object_or_404(Company, profile__id=kwargs['slug'])
        if company.status == 'w':
            serializer = CompanyProfileSerializer(company)
            if 'accept' in request.get_full_path():
                company.status = 'a'
            elif 'reject' in request.get_full_path():
                company.status = 'r'
            else:
                raise Http404
            company.save()
            data = serializer.data
            statusResponse = status.HTTP_200_OK
        else:
            raise ValidationError('Previously reviewed!')

        return Response(data=data, status=statusResponse)


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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get profile's EducationalBackground"""
        id = self.kwargs['slug']
        company = get_object_or_404(Employee, profile__id=id)
        education = company.educationalBackground.all()
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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get profile's WorkExperience"""
        slug = self.kwargs['slug']
        company = get_object_or_404(Wallet, id=slug)
        achievement = company.workExperience.all()
        return achievement


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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get profile's Achievment"""
        id = self.kwargs['slug']
        company = get_object_or_404(Wallet, id=id)
        achievement = company.achievement.all()
        return achievement


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
    pagination_class = StandardResultsSetPagination

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
        except:
            employee = profile.employee
            return serializer.save(employee=employee, sender='e', status='w')

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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get profile's Job Offer"""
        authID = self.kwargs['slug']
        if 'status' in self.request.data:
            if self.request.data['status'] in ['w', 'r', 'a']:
                qs = ApplyForJob.objects.filter(
                    Q(company__profile__id=authID) | Q(employee__profile__id=authID),
                    status=self.request.data['status'])
            else:
                qs = ApplyForJob.objects.filter(
                    Q(company__profile__id=authID) | Q(employee__profile__id=authID))
        else:
            qs = ApplyForJob.objects.filter(Q(company__profile__id=authID) | Q(employee__profile__id=authID))
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


class ReportReasonAPI(GenericAPIView, CreateModelMixin,
                      RetrieveModelMixin, DestroyModelMixin,
                      UpdateModelMixin):
    serializer_class = ReportReasonsSerializer
    queryset = ReportReason.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Report Reason By Admin"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Report Reason By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Report Reason By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Report Reason By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.destroy(request, *args, **kwargs)


class AllReportReasonsAPI(ListAPIView):
    """Get All Report Reason"""
    serializer_class = ReportReasonsSerializer
    queryset = ReportReason.objects.all()
    pagination_class = StandardResultsSetPagination


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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """get profile job offer"""
        profile = FindWallet(self.kwargs['slug'])
        company = GetCompany(profile)
        qs = company.jobOffer.all()
        return qs


class ReportAPI(GenericAPIView, CreateModelMixin,
                RetrieveModelMixin, DestroyModelMixin):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Report Reason By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Report Reason By Admin"""
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Report Reason By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        if serializer.validated_data.get('type') in ('p', 'c', 'q', 'a', 'w'):
            return serializer.save(reporter=GetWallet(self.request))
        else:
            raise ValidationError('the type is wrong')


class ReportsAPI(ListAPIView):
    """Get All Reports"""
    serializer_class = ReportSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    # Search Fields
    filterset_fields = ['type', 'slug']
    queryset = Report.objects.all()


class SearchJobOffers(ListAPIView):
    serializer_class = JobOfferSerializer
    queryset = JobOffer.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    """Search Fields"""
    filterset_fields = ['title', 'job', 'tech', 'category', 'count', 'jobType', 'text']


class SearchCompany(ListAPIView):
    serializer_class = CompanyProfileSerializer
    queryset = Company.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['companyName', 'about', 'foundedIn', 'employeeCount', 'industries', 'category', 'needEmployee']

class CompanyAll(ListAPIView):
    serializer_class = CompanySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['foundedIn', 'category', 'industries']
    queryset = Company.objects.all()


class CompanyRU(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = CompanySerializer
    permission_classes = [OwnerOrReadOnly]
    queryset = Company.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class EmployeeAll(ListAPIView):
    serializer_class = EmployeeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'category', 'industries',
                        'relationshipStatus', 'jobSearchStatus']
    queryset = Employee.objects.all()


class EmployeeRU(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = EmployeeSerializer
    permission_classes = [OwnerOrReadOnly]
    queryset = Employee.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
