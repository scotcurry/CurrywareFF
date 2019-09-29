from django.db import models
from django_unixdatetimefield import UnixDateTimeField


# Create your models here.
class OAuthInfo(models.Model):
    xoauth_yahoo_guid = models.CharField(max_length=40)
    access_token = models.CharField(max_length=1024)
    refresh_token = models.CharField(max_length=64, null=True)
    last_expire_time = UnixDateTimeField(verbose_name='ReFreshTime', null=True)

    def __str__(self):
        return self.access_token
