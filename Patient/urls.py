from django.urls import path, re_path, include

from . import views
from rest_framework.urlpatterns import format_suffix_patterns





urlpatterns = [
    path('', views.index, name='P_index'),
    path('signup/', views.signup, name='P_signup'),
    path('login/', views.loginform, name='P_login'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='P_activate'),
    path('profile/', views.profile_page, name='P_profile'),
    path('ajax/load-areas/', views.load_areas, name='P_ajax_load_areas'),
    path('symptoms/', views.symptoms, name='P_symptoms'),
    path('edit-profile/', views.edit_profile, name='P_edit_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('searchdoctor/', views.doctorSearchView, name='searchDoctor'),

    path('bookappointment/<docID>/', views.AppointmentBooking, name="bookAppointment"),
    path('confirmbooking/', views.confirmBooking, name="confirmBooking"),
    # path('predict/', views.input_symptoms, name="predictDisease"),
    path('predict/', views.DiseasePredict, name="predict"),
]
