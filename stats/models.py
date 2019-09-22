from django.db import models
from django_unixdatetimefield import UnixDateTimeField


# Create your models here.
class OAuthInfo(models.Model):
    token_id = models.IntegerField(default=1)
    access_token = models.CharField(max_length=1024)
    refresh_token = models.CharField(max_length=45)
    last_expire_time = UnixDateTimeField()

    def __str__(self):
        return self.access_token
