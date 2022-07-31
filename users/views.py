from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, GenericAPIView, \
    ListCreateAPIView

from posts.permission import IsItOwner
from users.permission import IsItOwnerCompany, ReadOnly, IsItEmployee
from users.serializer import *
from users.utils import GetCompany


class MyUserAPI(RetrieveAPIView):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        """Get Wallet"""
        return self.retrieve(request, *args, **kwargs)


class FollowAPI(ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    lookup_field = 'username'

    def post(self, request, *args, **kwargs):
        """Follow"""
        profile = request.user
        following = self.get_object()
        if following != profile:
            profile.following.add(following)
            notif = Notification(profile=following,
                                 text=f'{profile.id} followed you!', )
            notif.save()
        else:
            raise ValidationError('You cant follow yourself')
        return self.list(request, *args, **kwargs)


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


class IndustriesAPI(GenericAPIView):
    serializer_class = IndustriesSerializer
    queryset = Industry.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset().get_or_create(title=kwargs['title'])[0]
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GetAllIndustriesAPI(ListAPIView):
    """Get All Industries"""
    serializer_class = IndustriesSerializer
    filterset_fields = ['title']
    ordering_fields = '__all__'
    queryset = Industry.objects.all()


class CategoryAPI(RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GetAllCategoryAPI(ListCreateAPIView):
    """Get All Categories"""
    serializer_class = CategorySerializer
    filterset_fields = ['title', 'industry', 'upperCategory']
    ordering_fields = '__all__'
    queryset = Category.objects.all()


class TechAPI(RetrieveAPIView):
    serializer_class = TechSerializer
    queryset = Tech.objects.all()


class GetAllTechAPI(ListCreateAPIView):
    """Get All Techs"""
    serializer_class = TechSerializer
    filterset_fields = ['title', 'industry']
    queryset = Tech.objects.all()


class JobAPI(RetrieveAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()


class GetAllJobAPI(ListCreateAPIView):
    """Get All Jobs"""
    serializer_class = JobSerializer
    filterset_fields = ['title', 'industry']
    queryset = Job.objects.all()


class EducationalBackgroundAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = EducationalBackgroundSerializer
    queryset = EducationalBackground.objects.all()

    def put(self, request, *args, **kwargs):
        """Edit EducationalBackground"""
        self.permission_classes = [IsItEmployee]
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Edit EducationalBackground"""
        self.permission_classes = [IsItEmployee]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete EducationalBackground"""
        self.permission_classes = [IsItEmployee]
        return self.destroy(request, *args, **kwargs)


class EducationalBackgroundListAPI(ListCreateAPIView):
    serializer_class = EducationalBackgroundSerializer
    queryset = EducationalBackground.objects.all()
    filterset_fields = {
        'profile': ['exact'],
        'grad': ['exact', 'contains'],
        'major': ['exact', 'contains'],
        'educationalInstitute': ['exact', 'contains'],
        'start': ['exact', 'contains', 'lte', 'gte'],
        'end': ['exact', 'contains', 'lte', 'gte'],
        'adjusted': ['exact', 'lte', 'gte'],
        'description': ['exact', 'contains']
    }
    ordering_fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set Profile"""
        try:
            employee = self.request.user.employee
            return serializer.save(profile=employee)
        except Employee.DoesNotExist:
            raise ValidationError('There is no employee on this profile')


class WorkExperienceAPI(RetrieveUpdateDestroyAPIView):
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


class WorkExperienceListAPI(ListCreateAPIView):
    serializer_class = WorkExperienceSerializer
    queryset = WorkExperience.objects.all()
    filterset_fields = {
        'profile': ['exact'],
        'title': ['exact', 'contains'],
        'company': ['exact', 'contains'],
        'start': ['exact', 'contains', 'lte', 'gte'],
        'end': ['exact', 'contains', 'lte', 'gte'],
        'tech': ['contains'],
        'description': ['exact', 'contains']
    }
    ordering_fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set Profile"""
        return serializer.save(profile=self.request.user)


class AchievementAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = AchievementSerializer
    queryset = Achievement.objects.all()


    def put(self, request, *args, **kwargs):
        """Edit Achievement"""
        self.permission_classes = [IsItOwner]
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Edit Achievement"""
        self.permission_classes = [IsItOwner]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Achievement"""
        self.permission_classes = [IsItOwner]
        return self.destroy(request, *args, **kwargs)


class AchievementLIstAPI(ListCreateAPIView):
    serializer_class = AchievementSerializer
    queryset = Achievement.objects.all()
    filterset_fields = {
        'profile': ['exact'],
        'title': ['exact', 'contains'],
        'siteAddress': ['exact', 'contains'],
        'certificateProvider': ['exact', 'contains'],
        'date': ['exact', 'contains', 'lte', 'gte'],
        'description': ['exact', 'contains']
    }
    ordering_fields = '__all__'
    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.create(request, *args, **kwargs)
    def perform_create(self, serializer):
        """Set Profile"""
        return serializer.save(profile=self.request.user)


class NotificationMarkAsRead(RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Mark Notification as Read"""
        profile = request.user
        notification = self.get_object()
        if notification.profile == profile:
            notification.markAsRead = True
            notification.save()
            return self.retrieve(request, *args, **kwargs)
        else:
            raise ValidationError('access denied!')


class UserNotificationListAPI(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = '__all__'
    filterset_fields = {
        'profile': ['exact', ],
        'text': ['exact', 'contains'],
        'slug': ['exact', 'contains'],
        'date': ['exact', 'contains', 'lte', 'gte'],
        'markAsRead': ['exact', ]
    }

    def get_queryset(self):
        """Get User's Notifications"""
        profile = self.request.user
        notifications = profile.notification.all()
        return notifications


class ApplyForJobAPI(UpdateAPIView, RetrieveAPIView):
    serializer_class = ApplyForJobSerializer
    queryset = ApplyForJob.objects.all()

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


class AppliesForJobListAPI(ListCreateAPIView):
    serializer_class = ApplyForJobSerializer
    queryset = ApplyForJob.objects.all()
    ordering_fields = '__all__'
    filterset_fields = {
        'employee': ['exact', ],
        'company': ['exact', ],
        'sender': ['exact', ],
        'text': ['exact', 'contains'],
        'status': ['exact'],
        'nonCooperation': ['exact'],
        'nonCooperationDate': ['exact', 'contains', 'lte', 'gte']
    }

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.create(request, *args, **kwargs)

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


class JobOfferAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = JobOfferSerializer
    queryset = JobOffer.objects.all()

    def put(self, request, *args, **kwargs):
        """Edit Job Offer"""
        self.permission_classes = [IsItOwnerCompany]
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Edit Job Offer"""
        self.permission_classes = [IsItOwnerCompany]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Job Offer"""
        self.permission_classes = [IsItOwnerCompany]
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save(company=self.get_object().company)


class JobOfferListAPI(ListCreateAPIView):
    serializer_class = JobOfferSerializer
    queryset = JobOffer.objects.all()
    filterset_fields = ['title', 'job', 'tech', 'category', 'count', 'jobType', 'text']
    ordering_fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set Company on instance"""
        profile = self.request.user
        company = GetCompany(profile)
        return serializer.save(company=company)


class CompanyAll(ListAPIView):
    serializer_class = CompanyProfileSerializer
    queryset = Company.objects.all()
    filterset_fields = ['companyName', 'about', 'foundedIn', 'employeeCount', 'industries', 'category', 'needEmployee']
    ordering_fields = '__all__'


class EmployeeAll(ListAPIView):
    serializer_class = EmployeeSerializer
    filterset_fields = ['gender', 'category', 'industries',
                        'relationshipStatus', 'jobSearchStatus']
    queryset = Employee.objects.all()
    ordering_fields = '__all__'


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
