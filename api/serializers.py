from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.conf import settings
from social_core.exceptions import MissingBackend
from social_core.backends.utils import get_backend

from iotupdate.models import *


class TransactionSerializer(serializers.Serializer):
    device = serializers.CharField()
    version = serializers.CharField()
    data = serializers.CharField()


class DeviceTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceTemp
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class RollbackLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RollbackLog
        fields = '__all__'
