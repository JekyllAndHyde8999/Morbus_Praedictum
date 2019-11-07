from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

import sys
from Patient.models import City, Area
from Corporate.models import Company

GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Transgender'),
    (4, 'Other')
)

DAYS = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
)

INTERVALS = (
    (1, '15 Minutes'),
    (2, '30 Minutes'),
    (3, '45 Minutes'),
)

class Doctor(models.Model):
    Doctor_ID = models.AutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Doctor_First_Name = models.CharField(max_length=200)
    Doctor_Last_Name = models.CharField(max_length=200)
    Doctor_DOB = models.DateField(max_length=8)
    Doctor_Phone_Number = PhoneNumberField(max_length=13)
    Doctor_Email = models.EmailField()
    Doctor_Gender = models.IntegerField(choices=GENDER_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(4)])
    Doctor_Qualifications = models.CharField(max_length=350)
    Doctor_Specialization = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    Doctor_Experience = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(80)])
     # Doctor_License =
    Doctor_Picture = models.ImageField(upload_to='media', default='default-user-image.jpg', null=True)
    Doctor_Corporate = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default=None, blank=True)
    Doctor_Activate = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ClinicAddress(models.Model):
    Address_ID = models.AutoField(primary_key=True)
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Home = models.CharField(max_length=250)
    Street = models.CharField(max_length=250)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    Pin = models.CharField(max_length=6, default=000000)


class DoctorRating (models.Model):
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])


class TimeSlots(models.Model):
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Day = models.IntegerField(choices=DAYS, validators=[MinValueValidator(1), MaxValueValidator(7)])
    Opening_Time = models.TimeField()
    Closing_Time = models.TimeField()
    Interval = models.IntegerField(choices=INTERVALS, validators=[MinValueValidator(1), MaxValueValidator(3)])