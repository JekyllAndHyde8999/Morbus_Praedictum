from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Transgender'),
    (4, 'Other')
)

BLOOD_GROUP_CHOICES = (
    (1, "A+"),
    (2, "A-"),
    (3, "B+"),
    (4, "B-"),
    (5, "O+"),
    (6, "O-"),
    (7, "AB+"),
    (8, "AB-"),
)

BLOOD_DONATION = (
    (0, "Yes"),
    (1, "No")
)


# Create your models here.
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    Address_ID = models.AutoField(primary_key=True)
    Home = models.CharField(max_length=250)
    Street = models.CharField(max_length=250)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    Pin = models.CharField(max_length=6, default=000000)


class Profile(models.Model):
    Patient_ID = models.AutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Patient_First_Name = models.CharField(max_length=200)
    Patient_Last_Name = models.CharField(max_length=200)
    Patient_Phone_Number = PhoneNumberField(max_length=13)
    Patient_Picture = models.ImageField(upload_to='media', default='default-user-image.jpg', null=True)
    Patient_Gender = models.IntegerField(choices=GENDER_CHOICES, validators=[MinValueValidator(1),MaxValueValidator(4)])
    Patient_DOB = models.DateField(max_length=8)
    Patient_Blood_Group = models.IntegerField(choices=BLOOD_GROUP_CHOICES, validators=[MinValueValidator(1),MaxValueValidator(8)])
    Patient_Blood_Donation = models.IntegerField(choices=BLOOD_DONATION, validators=[MinValueValidator(0),MaxValueValidator(1)])
    Patient_Email = models.EmailField()
    Patient_Address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

