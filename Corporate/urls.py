from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.index, name='C_index'),
    path('signup/', views.signup, name='C_signup'),
    path('login/', views.loginform, name='C_login'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='C_activate'),
    path('profile/', views.profile_page, name='C_profile'),
    path('ajax/load-areas/', views.load_areas, name='C_ajax_load_areas'),
    path('edit-profile/', views.edit_profile, name='C_edit_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('adddoctor', views.addDoctor, name='C_addDoctor'),
    path('schedule', views.CorpDoctorScheduleView, name="addSchedule"),
    path('editschedule', views.editCorpDoctorSchedule, name="editSchedule"),
    
]