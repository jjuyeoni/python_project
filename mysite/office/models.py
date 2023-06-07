from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

CustomUser = get_user_model()

class UserInfoHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    alarmMsg = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
     return self.alarmMsg
