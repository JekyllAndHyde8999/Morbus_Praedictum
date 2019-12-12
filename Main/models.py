from django.db import models
from django.contrib.auth.models import User

from Doctor.models import Doctor
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Blog(models.Model):
    text = models.CharField(max_length=50000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=1000)

    class Meta:
       ordering = ('-date',)


class EyeDonor(models.Model):
    Name_of_Donor = models.CharField(max_length=50)
    time_of_death = models.TimeField()
    attendee_name = models.CharField(max_length=50)
    contact_info = PhoneNumberField(max_length=13)
    City = models.CharField(max_length=50)


class OrganDonor(models.Model):
    Name_of_Donor = models.CharField(max_length=50)
    attendee_name = models.CharField(max_length=50)
    contact_info = PhoneNumberField(max_length=13)
    City = models.CharField(max_length=50)
