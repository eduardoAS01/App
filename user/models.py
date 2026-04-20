from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from business.models import Business

class User(AbstractUser):
    email =  models.EmailField(unique=True)
    image = models.ImageField(upload_to='user/',blank=True,null=True)
    active_business = models.ForeignKey(Business,null=True,blank=True,on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
