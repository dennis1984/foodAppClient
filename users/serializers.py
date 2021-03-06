# -*- coding:utf8 -*-
import os

from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from Business_App.bz_users.models import BusinessUser
from horizon.serializers import (BaseListSerializer,
                                 timezoneStringTostring)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUser
        fields = '__all__'

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password is None:
            raise ValueError('Password is cannot be empty.')
        validated_data['password'] = make_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

    def update_password(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password is None:
            raise ValueError('Password is cannot be empty.')
        kwargs = {'password': make_password(password)}
        return super(UserSerializer, self).update(instance, kwargs)


class UserInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUser
        fields = ('id', 'phone', 'business_name', 'head_picture',
                  'food_court_id')


class UserDetailSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    phone = serializers.CharField(max_length=20)
    business_name = serializers.CharField(max_length=100)
    food_court_id = serializers.IntegerField()
    last_login = serializers.DateTimeField()

    head_picture = serializers.ImageField()
    food_court_name = serializers.CharField(max_length=200, required=False)
    city = serializers.CharField(max_length=100, required=False)
    district = serializers.CharField(max_length=100, required=False)
    mall = serializers.CharField(max_length=200, required=False)

    @property
    def data(self):
        _data = super(UserDetailSerializer, self).data
        if _data.get('user_id', None):
            _data['last_login'] = timezoneStringTostring(_data['last_login'])
            base_dir = _data['head_picture'].split('static', 1)[1]
            if base_dir.startswith(os.path.sep):
                base_dir = base_dir[1:]
            _data['head_picture_url'] = os.path.join(settings.WEB_URL_FIX,
                                                     'static',
                                                     base_dir)
        return _data


class UserListSerializer(BaseListSerializer):
    child = UserDetailSerializer()

