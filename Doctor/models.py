from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from datetime import time
from django.forms import formset_factory
import sys
from Patient.models import City, Area, Profile
from Corporate.models import Company

HOUR_CHOICES = [(time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Transgender'),
    (4, 'Other')
)

DAYS = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday')
)

INTERVALS = (
    (1, '15 Minutes'),
    (2, '30 Minutes'),
    (3, '45 Minutes'),
)

slotTimeChoices = (
    (10, '10 min'),
    (15, '15 min'),
    (20, '20 min'),
    (30, '30 min'),
    (60, '60 min')
)

TimeChoices = (
    ('00:00:00', '00:00'),
    ('00:30:00', '00:30'),
    ('01:00:00', '01:00'),
    ('01:30:00', '01:30'),
    ('02:00:00', '02:00'),
    ('03:00:00', '03:00'),
    ('04:00:00', '04:00'),
    ('05:00:00', '05:00'),
    ('06:00:00', '06:00'),
    ('07:00:00', '07:00'),
    ('08:00:00', '08:00'),
    ('09:00:00', '09:00'),
    ('10:00:00', '10:00'),
    ('11:00:00', '11:00'),
    ('12:00:00', '12:00'),
)


class ClinicAddress(models.Model):
    ClinicAddress_ID =  models.AutoField(primary_key=True, auto_created=True, default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    Home = models.CharField(max_length=250)
    Street = models.CharField(max_length=250)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    Pin = models.CharField(max_length=6, default=000000)


class Doctor(models.Model):
    Doctor_ID = models.AutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Doctor_First_Name = models.CharField(max_length=200)
    Doctor_Last_Name = models.CharField(max_length=200)
    Doctor_DOB = models.DateField(max_length=8)
    Doctor_Phone_Number = PhoneNumberField(max_length=13)
    Doctor_Email = models.EmailField(default="asd@rew.com")
    Doctor_Gender = models.IntegerField(choices=GENDER_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(4)])
    Doctor_Qualifications = models.CharField(max_length=350)
    Doctor_Specialization = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    Doctor_Experience = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(80)])
    Doctor_License = models.CharField(default='1234567890', max_length=25, null=True)
    Doctor_Picture = models.ImageField(upload_to='media', default='default-user-image.jpg', null=True)
    Doctor_Corporate = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default=None, blank=True)
    Doctor_Activate = models.BooleanField(default=False)
    Doctor_Address = models.ForeignKey(ClinicAddress, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class DoctorRating (models.Model):
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[MinValueValidator(0), MaxValueValidator(5)])


class TimeSlots(models.Model):
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE, name="Doctor_ID")
    Patient_ID = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, name="Patient_ID")
    day = models.CharField(max_length=10, choices=DAYS)
    date = models.DateField()
    opening_Time = models.TimeField()

    def __str__(self):
        return self.Doctor_ID.user.username


class doctorSchedule(models.Model):
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, name="Doctor_ID")
    day = models.CharField(max_length=10)
    interval = models.IntegerField(choices=slotTimeChoices, default='10')
    openTime = models.TimeField(choices=HOUR_CHOICES)
    closeTime = models.TimeField(choices=HOUR_CHOICES)

    class Meta:
        db_table = 'schedule'

    def __str__(self):
        return self.Doctor_ID.user.username


# class appointmentBooking(models.Model):
#     docUsername = models.CharField(max_length=40)
#     day = models.CharField(max_length=10)
#     slotTime = models.TimeField(auto_now=False )
#     patientUsername = models.CharField(max_length=40)
#
#     def __str__(self):
#         return self.docUsername
