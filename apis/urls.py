from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('schedule/', views.scheduleApiView.as_view(), name="scheduleAPI"),
    path('doctors/', views.DoctorApi.as_view(), name="doctorList"),
    path('patients/', views.DonorList.as_view(), name="donor-all"),
    path('predict/', views.DiseasePredictor.as_view(), name="predictAPI"),
    path('timeslots/', views.timeSlotsApiView.as_view(), name="TimeSlotsAPI"),
    path('auth/login/', views.loginViewAPI.as_view(), name="loginAPI"),
    path('auth/logout/', views.logoutViewAPI.as_view(), name="logoutAPI"),
    path('c_adddoctor', views.addDoctorView.as_view(), name="addDoctor")
    ]
