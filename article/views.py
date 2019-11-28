from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from article.models import Article
from article.serializers import ArticleSerializer, ArticleCreateSerializer




class ArticleViewSet(CreateModelMixin,
                     ListModelMixin,
                     UpdateModelMixin,
                     RetrieveModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):
    class _Permission(BasePermission):
        def has_permission(self, request, view):
            if not request.session.get('uid'):
                return False
            return True

    serializer_class = ArticleCreateSerializer
    queryset = Article.objects.all()
    permission_classes = [_Permission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)


