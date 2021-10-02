from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin,
                                   UpdateModelMixin)

from authentication.permission import IsAdmin
from users.models import *
from users.serializer import ReportReasonsSerializer, ReportSerializer
from users.utils import GetWallet


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
        if serializer.validated_data.get('type') in ('p',  'c',  'q', 'a', 'w'):
            return serializer.save(reporter=GetWallet(self.request))
        else:
            raise ValidationError('the type is wrong')


class ReportsAPI(ListAPIView):
    serializer_class = ReportSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Get All Reports"""
        if 'type' in self.request.data:
            return Report.objects.filter(type=self.request.data['type'])

        if 'slug' in self.request.data:
            return Report.objects.filter(slug=self.request.data['slug'])

        return Report.objects.all()
