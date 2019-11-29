from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from article.models import Article
from article.serializers import ArticleSerializer, ArticleCreateSerializer
from codinglife.filters import CustomSearchFilter
from codinglife.mixins import DDArticleListModelMixin


class ArticleViewSet(CreateModelMixin,
                     # ListModelMixin,
                     DDArticleListModelMixin,
                     UpdateModelMixin,
                     RetrieveModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):
    class _Permission(BasePermission):
        def has_permission(self, request, view):
            if request.session.get('uid') or request.method in SAFE_METHODS:
                return True
            return False

    serializer_class = ArticleCreateSerializer
    queryset = Article.objects.all()
    permission_classes = [_Permission]
    filter_backends = [DjangoFilterBackend, CustomSearchFilter, OrderingFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content', 'user__username', 'user__email']
    ordering_fields = ['id', 'title']
    ordering = 'id'



