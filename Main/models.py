from django.db import models
from django.contrib.auth.models import User

from Doctor.models import Doctor
# Create your models here.

class Blog(models.Model):
    text = models.CharField(max_length=50000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=1000)

    class Meta:
       ordering = ('-date',)
