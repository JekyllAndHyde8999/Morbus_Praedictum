from django.db import models

# Create your models here.


class Feedback(models.Model):
    username = models.CharField(max_length=40)
    feedback = models.CharField(max_length=500)
    #date = models.DateField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username