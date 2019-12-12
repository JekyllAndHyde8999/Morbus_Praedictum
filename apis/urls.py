from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('doctor/viewschedule/', views.viewDoctorScheduleApiView.as_view(), name="scheduleAPI"),  # view Doctor's schedule
    path('doctor/addschedule/', views.addDoctorScheduleApiView.as_view(), name="scheduleAPI"),  # Add Doctor's schedule
    path('doctors/', views.DoctorApi.as_view(), name="doctorList"),                     # SERVICE view All Doctors available for recruitment
    path('patients/', views.DonorList.as_view(), name="donor-all"),                     # SERVICE view all Blood donors
    path('predict/', views.DiseasePredictor.as_view(), name="predictAPI"),              # SERVICE disease prediction API
    path('timeslots/', views.timeSlotsApiView.as_view(), name="TimeSlotsAPI"),
    path('auth/login/', views.loginViewAPI.as_view(), name="loginAPI"),
    path('auth/logout/', views.logoutViewAPI.as_view(), name="logoutAPI"),
    path('corp/adddoctor/', views.addDoctorView.as_view(), name="addDoctor"),
    path('corp/viewschedule/', views.viewCorpDoctorScheduleApiView.as_view(), name="viewCorpDoctorSchedule"),
    ]
