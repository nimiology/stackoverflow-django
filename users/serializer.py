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
        model = Industry
        fields = '__all__'


class VerifyIndustriesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)

    class Meta:
        model = Industry
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


class MyUserSerializer(serializers.ModelSerializer):
    employee = EmployeeProfileSerializer(read_only=True)
    company = CompanyProfileSerializer(read_only=True)

    class Meta:
        model = MyUser
        fields = '__all__'


class WorkExperienceSerializer(serializers.ModelSerializer):
    profile = MyUserSerializer(required=False, read_only=True)

    class Meta:
        model = WorkExperience
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['tech'] = TechSerializer(many=True, read_only=True)
        return super(WorkExperienceSerializer, self).to_representation(instance)


class AchievementSerializer(serializers.ModelSerializer):
    profile = MyUserSerializer(required=False, read_only=True)

    class Meta:
        model = Achievement
        fields = '__all__'


class FollowingSerializer(serializers.ModelSerializer):
    following = MyUserSerializer(many=True, read_only=True)

    class Meta:
        model = MyUser
        fields = ['following']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['profile'] = MyUserSerializer(read_only=True)
        return super(NotificationSerializer, self).to_representation(instance)


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


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {'profile': {'required': False}}


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {'profile': {'required': False}}
