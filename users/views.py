from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permission import IsAdmin, OwnerOrReadOnly
from users.serializer import *
from users.utils import GetWallet, FindWallet


class WalletAPI(GenericAPIView, RetrieveModelMixin):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Wallet"""
        return self.retrieve(request, *args, **kwargs)


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
        """Confirm Follow Request"""
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
                followRequest = FollowRequest(
                    sender=profile, receiver=following)
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
        """Get Report Reason By Admin"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Report Reason By Admin"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit Report Reason By Admin"""
        self.serializer_class = VerifyIndustriesSerializer
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete Report Reason By Admin"""
        self.permission_classes = [IsAdmin]
        self.check_permissions(self.request)
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        GetWallet(self.request)
        return serializer.save(status='w')


class GetAllIndustriesAPI(ListAPIView):
    serializer_class = IndustriesSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'status']
    queryset = Industries.objects.all()


class CategoryAPI(GenericAPIView, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Category By Admin"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Category By Admin"""
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
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'industry__title',
                        'upperCategory__title', 'status']
    queryset = Category.objects.all()


class TechAPI(GenericAPIView, CreateModelMixin,
              RetrieveModelMixin, UpdateModelMixin,
              DestroyModelMixin):
    serializer_class = TechSerializer
    queryset = Tech.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Tech By Admin"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Tech By Admin"""
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
    serializer_class = TechSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'industry__title']
    queryset = Tech.objects.all()


class JobAPI(GenericAPIView, CreateModelMixin,
             RetrieveModelMixin, UpdateModelMixin,
             DestroyModelMixin):
    serializer_class = JobSerializer
    queryset = Job.objects.all()

    def get(self, request, *args, **kwargs):
        """Get Tech By Admin"""
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create Tech By Admin"""
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


class GetAllJobAPI(ListAPIView):
    serializer_class = JobSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
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
    serializer_class = ReportReasonsSerializer
    queryset = ReportReason.objects.all()
    pagination_class = StandardResultsSetPagination


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
    serializer_class = ReportSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'slug']
    queryset = Report.objects.all()


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
