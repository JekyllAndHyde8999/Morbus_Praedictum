from django.shortcuts import render
# import schedule
# import time as t
# import datetime
# Create your views here.
# from Doctor.models import *
# from django.utils import timezone
# from Doctor.views import get_date
#
from datetime import datetime, timedelta
from threading import Timer


# def trigger_updatedoctorslots():
#     doctors = doctorSchedule.objects.filter(day=timezone.now().day)
#     print("deleting previous day slots");
#     TimeSlots.objects.filter(date__lte=timezone.now().date()).delete()
#     print("deleted previous day slots");
#     for i in doctors:
#         start_time = str(i.openTime)
#         end_time = str(i.closeTime)
#         slot_time = i.interval
#         day = i.day
#         docID = i.Doctor_ID
#         time = datetime.datetime.strptime(start_time, '%H:%M:%S')
#         end = datetime.datetime.strptime(end_time, '%H:%M:%S')
#         while time <= end:
#             op_time = time.time()
#             date = get_date(datetime.datetime.today(), day)
#             TimeSlots(Doctor_ID=docID, day=day, date=date, opening_Time=op_time).save()
#             time += datetime.timedelta(minutes=slot_time)
#
# schedule.every().second.do(trigger_updatedoctorslots)

# while True:
#     schedule.run_pending()
#      #t.sleep(1000)


# Create your views here.
def index(request):
    
    return render(request, 'Main/index copy.html')

def index1(request):
    return render(request, 'Main/login.html')

def index2(request):
    return render(request, 'Main/signup.html')
