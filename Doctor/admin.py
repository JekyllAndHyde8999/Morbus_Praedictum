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

#     if day:
#         user_object = User.objects.get(username=request.user.username)
#         docID = Doctor.objects.get(user=user_object)
#         if m_openTime and m_closeTime and m_interval:
#             doctorSchedule(Doctor_ID=docID, day=day, openTime=m_openTime, closeTime=m_closeTime,
#                            interval=m_interval).save()
#
#         if e_openTime and e_closeTime and e_interval:
#             doctorSchedule(Doctor_ID=docID, day=day, openTime=e_openTime, closeTime=e_closeTime,
#                            interval=e_interval).save()
#
#
# docUsername = request.user.username