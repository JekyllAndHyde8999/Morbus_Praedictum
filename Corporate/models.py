from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from Patient.models import City, Area

# Create your models here.
class HospitalAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    Address_ID = models.AutoField(primary_key=True)
    Home = models.CharField(max_length=250)
    Street = models.CharField(max_length=250)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    Pin = models.CharField(max_length=6, default=000000)


class Company(models.Model):
    Comapny_ID = models.AutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Company_Name = models.CharField(max_length=250)
    Company_License_Number = models.CharField(max_length=250)
    Company_Phone_Number = PhoneNumberField(max_length=13)
    Company_Email = models.EmailField()
    Company_Address = models.ForeignKey(HospitalAddress, on_delete=models.CASCADE)
    Company_Logo = models.ImageField(upload_to='media', default='default-user-image.jpg', null=True)
    Company_Activate = models.BooleanField(default=False)
