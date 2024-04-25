from django.db import models
from django.contrib.auth.models import AbstractUser

class Post(models.Model):
    writer = models.TextField(null=False)
    title = models.TextField(null=False)
    content = models.TextField(null=False)
    writetime = models.DateField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

