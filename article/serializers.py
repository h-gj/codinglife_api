from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from article.models import Article
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
        fields = ['title', 'content', 'user']


