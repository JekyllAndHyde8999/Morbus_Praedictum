from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from datetime import time
from django.forms import formset_factory
import sys

from Patient.models import Area, City

class HospitalAddress(models.Model):
    HospitalAddress_ID = models.AutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    Home = models.CharField(max_length=250)
    Street = models.CharField(max_length=250)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    Pin = models.CharField(max_length=6, default=000000)


class Company(models.Model):
    Company_ID = models.AutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Company_Name = models.CharField(max_length=200)
    Company_Phone_Number = PhoneNumberField(max_length=13)
    Company_Email = models.EmailField(default="asd@rew.com")
    Company_License_Number = models.CharField(default='1234567890', max_length=25, null=True)
    Company_Logo = models.ImageField(upload_to='media', default='default-user-image.jpg', null=True)
    Company_Activate = models.BooleanField(default=False)
    Company_Address = models.ForeignKey(HospitalAddress, on_delete=models.CASCADE, null=True)
