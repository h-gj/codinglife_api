from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from article.models import Article, ArticleComment
from article.serializers import ArticleSerializer, ArticleCreateSerializer, ArticleCommentSerializer, \
    ArticleCommentCreateSerializer
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


class ArticleCommentViewSet(CreateModelMixin,
                            ListModelMixin,
                            DestroyModelMixin,
                            GenericViewSet):
    serializer_class = ArticleCommentSerializer
    queryset = ArticleComment.objects.all()

    @swagger_auto_schema(request_body=ArticleCommentCreateSerializer)
    def create(self, request, *args, **kwargs):
        serializer = ArticleCommentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_QUERY,
            description='ID of the specified article.',
            required=True,
            type=openapi.TYPE_INTEGER,
        )])
    def list(self, request, *args, **kwargs):
        article_id = self.request.query_params.get('article_id')
        queryset = ArticleComment.objects.filter(article_id=article_id)
        return Response(self.get_serializer(queryset, many=True).data)
