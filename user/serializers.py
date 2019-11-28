from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from user.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        instance = self.Meta.model(**validated_data)
        instance.save()
        print('type of instance:', type(instance))
        return instance


class UserLoginSerializer(ModelSerializer):
    account = serializers.CharField(max_length=100, help_text="用户名或邮箱")

    class Meta:
        model = User
        fields = ['account', 'password']

    def validate(self, attrs):
        user = User.objects.get(Q(username=attrs['account']) | Q(email=attrs['account']))
        if check_password(attrs['password'], user.password):
            return attrs
        raise ValidationError(detail='账号或密码错误')


class UserEmptySerializer(Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
