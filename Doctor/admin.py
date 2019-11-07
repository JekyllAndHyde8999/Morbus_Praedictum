from django.contrib import admin
from .models import ClinicAddress, Doctor, DoctorRating, TimeSlots

# Register your models here.
admin.site.register(Doctor)
admin.site.register(ClinicAddress)
admin.site.register(DoctorRating)
admin.site.register(TimeSlots)