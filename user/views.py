from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, \
    RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import GenericViewSet

from user.models import User
from user.serializers import UserSerializer, UserCreateSerializer, UserLoginSerializer, UserEmptySerializer


class UserViewSet(CreateModelMixin,
                  ListModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(tags=['用户'], operation_summary='新建用户',
                         request_body=UserCreateSerializer)
    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(UserViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=['用户'], operation_summary='用户登陆',
                         request_body=UserLoginSerializer)
    @action(methods=['POST'], detail=False)
    def login(self, request, *arg, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(Q(username=serializer.validated_data['account']) |
                                    Q(email=serializer.validated_data['account']))
            request.session.cycle_key()
            request.session['uid'] = user.id
            return Response(UserSerializer(user).data)

    @swagger_auto_schema(tags=['用户'], operation_summary='退出登陆', request_body=UserEmptySerializer)
    @action(methods=['POST'], detail=False)
    def logout(self, request, *arg, **kwargs):
        request.session.flush()
        return Response()
