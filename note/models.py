from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

# Create your models here..

class User (models.Model):
     user_id = models.IntegerField(primary_key=True,null=False)
     name = models.CharField(max_length=32,null=False,unique = True)
     email = models.CharField(max_length=32,null=False,unique=True)
     ph = models.IntegerField()
  
     
class Note(models.Model):
     user_id = models.ForeignKey(User,on_delete= models.CASCADE)
     create_on = models.DateTimeField(auto_now_add=True)
     note = models.TextField()

              # This will say what to print in django admin
# class TokenUser (models.Model):
#      user_id = models.OneToOneField(User,on_delete=models.CASCADE)
#      toekn = models.TextField()
     


