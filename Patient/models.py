from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Profile(models.Model):
    Patient_ID = models.AutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Patient_First_Name = models.CharField(max_length=200)
    Patient_Last_Name = models.CharField(max_length=200)
    Patient_Phone_Number = PhoneNumberField(max_length=13)
    Patient_Picture = models.ImageField(upload_to='media', null=True)
    Patient_Gender = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(4)])
    Patient_DOB = models.DateField(max_length=8)
    Patient_Email = models.EmailField(default="asd@rew.com")

    def __str__(self):
        return self.user.username


class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Address(models.Model):
    Address_ID = models.AutoField(primary_key=True)
    Patient_ID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Home = models.CharField(max_length=250)
    Street = models.CharField(max_length=250)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    Pin = models.CharField(max_length=6, default=000000)




#DOB
#Age
#Gender