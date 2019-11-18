from django.db import models


# Create your models here.
class UserInfo(models.Model):
	username = models.CharField(max_length=32)
	password = models.CharField(max_length=64)
	token = models.CharField(max_length=128, null=True)
