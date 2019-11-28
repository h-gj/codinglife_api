from django.db import models

# Create your models here.
from user.models import User


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', related_name='articles', on_delete=models.CASCADE)
    is_modified = models.BooleanField(default=False)

