from rest_framework import serializers


class UserOTPCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
