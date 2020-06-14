from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_dinkes = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
    	return str(self.user)
    