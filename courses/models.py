from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    coutype= models.CharField(verbose_name='講座',max_length=50)
    coumask = models.CharField(verbose_name='資格',max_length=10,default='000')
    mon = models.IntegerField(verbose_name='月曜',default=3)
    tue = models.IntegerField(verbose_name='火曜',default=3)
    wed = models.IntegerField(verbose_name='水曜',default=3)

class Attendee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attended = models.CharField(verbose_name='完了',max_length=10,default='000')
    applicated = models.CharField(verbose_name='申込',max_length=10,default='000')
