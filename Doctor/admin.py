from django.contrib import admin
from .models import ClinicAddress, Doctor, DoctorRating, doctorSchedule, TimeSlots


class DocScheduleClass(admin.ModelAdmin):
    list_display = ['Doctor_ID', 'day', 'interval', 'openTime', 'closeTime']


class TimeSlotClass(admin.ModelAdmin):
    list_display = ['Doctor_ID', 'Patient_ID', 'day', 'date', 'opening_Time']
# Register your models here.
admin.site.register(Doctor)
admin.site.register(ClinicAddress)
admin.site.register(DoctorRating)
admin.site.register(TimeSlots, TimeSlotClass)

admin.site.register(doctorSchedule, DocScheduleClass)
