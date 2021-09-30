from rest_framework import serializers


class FilterSerializer(serializers.Serializer):
    filter = serializers.DictField(required=False)
    sort_by = serializers.CharField(required=False)
    sort_type = serializers.IntegerField(required=False)
    per_page = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)


class RegisterSrializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()


class LoginSrializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()


class UpdateSrializer(serializers.Serializer):

    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)


class DeleteSrializer(serializers.Serializer):

    password = serializers.CharField()


class RefreshTokenSrializer(serializers.Serializer):

    refresh_token = serializers.CharField()
