from django.db import models

# Create your models here.
from codinglife.models import BaseModel


class User(BaseModel):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)


