from django.db import models
from django.conf import settings

# Create your models here.
class Business(models.Model):
    
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


class BusinessMember(models.Model):

    ROLE_CHOICES = [
        ("owner","Owner"),
        ("employee","Employee")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,db_index=True)
    business = models.ForeignKey(Business,on_delete=models.CASCADE,related_name="members")
    role = models.CharField(max_length=50,choices=ROLE_CHOICES)