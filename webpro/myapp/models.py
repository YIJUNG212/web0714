from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.
class webUser(AbstractUser):
    phone = models.CharField(max_length=50,null=True,blank=False)
    addr = models.CharField(max_length=255,null=True,blank=False)
    hobit = models.CharField(max_length=255,null=True,blank=False)
    join_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.username}"
