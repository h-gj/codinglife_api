from django.db import models

# Create your models here.
from codinglife.models import BaseModel
from user.models import User


class Article(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey('user.User', related_name='articles', on_delete=models.CASCADE)
    is_modified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

