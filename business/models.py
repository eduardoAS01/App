from django.db import models
from django.conf import settings

# Create your models here.
class Business(models.Model):
    
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner","name"],
                name = "unique_owner_name"
            )
        ]


class BusinessMember(models.Model):

    ROLE_CHOICES = [
        ("owner","Owner"),
        ("employee","Employee")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,db_index=True)
    business = models.ForeignKey(Business,on_delete=models.CASCADE,related_name="members",db_index=True)
    role = models.CharField(max_length=50,choices=ROLE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user","business"],
                name = "unique_user_bussines"
            )
        ]