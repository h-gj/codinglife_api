from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from article.models import Article, ArticleComment
from user.models import User
from user.serializers import UserSerializer


class ArticleCreateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.user = self.context['request'].user
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.is_modified = True
        instance.save(update_fields=['is_modified'])
        super(ArticleCreateSerializer, self).update(instance, validated_data)
        return instance


class ArticleSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'user']


# class ArticleCommentCreateSerializer(Serializer):
#     # class Meta:
#     #     model = ArticleComment
#     #     fields = ['content', 'article']
#
#     content = serializers.CharField()
#     article_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         instance = ArticleComment(**validated_data)
#         instance.author = self.context['request'].user
#         instance.article = Article.objects.get(pk=validated_data.get('article_id'))
#         instance.save()
#         return instance


class ArticleCommentCreateSerializer(ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ['content', 'article']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super(ArticleCommentCreateSerializer, self).create(validated_data)


class ArticleCommentSerializer(ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = serializers.ALL_FIELDS

