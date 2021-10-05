from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from users.models import *


class TechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tech
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['industry'] = IndustriesSerializer(read_only=True)
        return super(TechSerializer, self).to_representation(instance)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['industry'] = IndustriesSerializer(read_only=True)
        return super(JobSerializer, self).to_representation(instance)


class IndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        fields = '__all__'


class VerifyIndustriesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)

    class Meta:
        model = Industries
        fields = '__all__'


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ReadOnlyField(source='profile.id')
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        self.fields['techWantsToWorkWith'] = TechSerializer(
            many=True, read_only=True)
        self.fields['techWantsToNotWorkWith'] = TechSerializer(
            many=True, read_only=True)
        self.fields['role'] = JobSerializer(many=True, read_only=True)
        self.fields['industries'] = IndustriesSerializer(
            many=True, read_only=True)
        self.fields['industriesToExclude'] = IndustriesSerializer(
            many=True, read_only=True)
        return super(EmployeeProfileSerializer, self).to_representation(instance)


class EducationalBackgroundSerializer(serializers.ModelSerializer):
    profile = EmployeeProfileSerializer(read_only=True)

    class Meta:
        model = EducationalBackground
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['industry'] = IndustriesSerializer(read_only=True)
        self.fields['upperCategory'] = ReadOnlyField(
            source='upperCategory.title')
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        return super(CategorySerializer, self).to_representation(instance)


class VerifyCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['industry'] = IndustriesSerializer(read_only=True)
        self.fields['upperCategory'] = ReadOnlyField(
            source='upperCategory.title')
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        return super(VerifyCategorySerializer, self).to_representation(instance)


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = ReadOnlyField(source='profile.id')
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        self.fields['industries'] = IndustriesSerializer(
            read_only=True, many=True)
        return super(CompanyProfileSerializer, self).to_representation(instance)


class JobOfferSerializer(serializers.ModelSerializer):
    company = CompanyProfileSerializer(required=False)

    class Meta:
        model = JobOffer
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['tech'] = TechSerializer(read_only=True, many=True)
        self.fields['category'] = CategorySerializer(read_only=True, many=True)
        return super(JobOfferSerializer, self).to_representation(instance)


class WalletSerializer(serializers.ModelSerializer):
    employee = EmployeeProfileSerializer(read_only=True)
    company = CompanyProfileSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = '__all__'


class WorkExperienceSerializer(serializers.ModelSerializer):
    profile = WalletSerializer(required=False)

    class Meta:
        model = WorkExperience
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['tech'] = TechSerializer(many=True, read_only=True)
        return super(WorkExperienceSerializer, self).to_representation(instance)


class AchievementSerializer(serializers.ModelSerializer):
    profile = WalletSerializer(required=False)

    class Meta:
        model = Achievement
        fields = '__all__'


class FollowingSerializer(serializers.ModelSerializer):
    following = WalletSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ['following']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = WalletSerializer(read_only=True)
        return super(NotificationSerializer, self).to_representation(instance)


class CompanyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDocument
        fields = '__all__'
        extra_kwargs = {'company': {'required': False}}

    def to_representation(self, instance):
        self.fields['company'] = CompanyProfileSerializer()
        return super(CompanyDocumentSerializer, self).to_representation(instance)


class ApplyForJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForJob
        fields = '__all__'
        extra_kwargs = {
            'sender': {'required': False},
            'company': {'required': False},
            'employee': {'required': False},

        }

    def to_representation(self, instance):
        self.fields['employee'] = EmployeeProfileSerializer(read_only=True)
        self.fields['company'] = CompanyProfileSerializer(read_only=True)
        return super(ApplyForJobSerializer, self).to_representation(instance)


class ReportReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    reporter = WalletSerializer(read_only=True, required=False)

    class Meta:
        model = Report
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['reason'] = ReportReasonsSerializer(read_only=True)
        return super(ReportSerializer, self).to_representation(instance)


class FollowRequestSerializer(serializers.ModelSerializer):
    sender = WalletSerializer(read_only=True, required=False)
    receiver = WalletSerializer(read_only=True, required=False)

    class Meta:
        model = FollowRequest
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['profilePic', 'companyName', 'about', 'workEmail', 'phoneNumber', 'website',
                  'foundedIn', 'category', 'industries', 'employeeCount', 'needEmployee', 'status']


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['name', 'profilePic', 'category', 'about',
                  'address', 'phoneNumber',
                  'birthday', 'gender', 'relationshipStatus', 'jobSearchStatus',
                  'minimumAnnualSalary', 'techWantsToWorkWith',
                  'techWantsToNotWorkWith', 'role', 'industries', 'industriesToExclude',
                  'jobType', 'hire']
