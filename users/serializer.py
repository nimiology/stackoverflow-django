from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from users.models import *


class TechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tech
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class IndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        fields = '__all__'


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        self.fields['tech'] = TechSerializer(many=True, read_only=True)
        return super(WorkExperienceSerializer, self).to_representation(instance)


class EducationalBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalBackground
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        return super(EducationalBackgroundSerializer, self).to_representation(instance)


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        return super(AchievementSerializer, self).to_representation(instance)


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ReadOnlyField(source='profile.id')
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        self.fields['techWantsToWorkWith'] = TechSerializer(many=True, read_only=True)
        self.fields['techWantsToNotWorkWith'] = TechSerializer(many=True, read_only=True)
        self.fields['role'] = RoleSerializer(many=True, read_only=True)
        self.fields['industries'] = IndustriesSerializer(many=True, read_only=True)
        self.fields['industriesToExclude'] = IndustriesSerializer(many=True, read_only=True)
        return super(EmployeeProfileSerializer, self).to_representation(instance)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['upperCategory'] = ReadOnlyField(source='upperCategory.title')
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        return super(CategorySerializer, self).to_representation(instance)


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ReadOnlyField(source='profile.id')
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        self.fields['industries'] = IndustriesSerializer(read_only=True, many=True)
        return super(CompanyProfileSerializer, self).to_representation(instance)


class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['company'] = CompanyProfileSerializer(read_only=True)
        self.fields['tech'] = TechSerializer(read_only=True, many=True)
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        return super(JobOfferSerializer, self).to_representation(instance)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['employeeProfile'] = EmployeeProfileSerializer(read_only=True)
        self.fields['companyProfile'] = CompanyProfileSerializer(read_only=True)
        return super(ProfileSerializer, self).to_representation(instance)


class FollowingSerializer(serializers.ModelSerializer):
    following = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ['following']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        return super(NotificationSerializer, self).to_representation(instance)


class CompanyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDocument
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['company'] = CompanyProfileSerializer()
        return super(CompanyDocumentSerializer, self).to_representation(instance)


class ApplyForJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForJob
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['employee'] = EmployeeProfileSerializer(read_only=True)
        self.fields['company'] = CompanyProfileSerializer(read_only=True)
        return super(ApplyForJobSerializer, self).to_representation(instance)


class ReportReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['reporter'] = ProfileSerializer(read_only=True)
        self.fields['reasons'] = ReportReasonsSerializer(read_only=True)
        return super(ReportSerializer, self).to_representation(instance)
