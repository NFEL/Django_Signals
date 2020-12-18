from django.db import models
from django.contrib.auth.models import User

## Uncomment here to use signal instead of save() function
## میتونید این قسمت رو ان کامنت کنید و بجای متد سیو استفاده کنید .

# from django.db.models.signals import pre_save
# from django.dispatch.dispatcher import receiver

# @receiver(pre_save,sender= Profile)
# def create_user_before_profile_saves(instance,*args, **kwargs):
#     try:
#         user = User.objects.create(username = f'{instance.ful_name} - {instance.phonenumber}',password=instance.password) 
#         instance.id = user
#     except Exception:
#         raise Exception



class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.RESTRICT,primary_key=True,blank=True)
    password = models.CharField(max_length=128,blank=True, null=True)
    ful_name = models.CharField(max_length=40, null=False)
    phonenumber = models.CharField(max_length=12, null=False,unique=True)
    
    def save(self,*args, **kwargs):
        try:
            if not self.password:
                password = User.objects.make_random_password()
                print(password)
            else:
                password = self.password
            user = User.objects.create(username = f'{self.ful_name} - {self.phonenumber}',password=password) 
            self.user_id = user
        except Exception as e:
            raise e
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.ful_name:
            return f'{self.ful_name} - {self.phonenumber}'
        else:
            return str(self.id)
