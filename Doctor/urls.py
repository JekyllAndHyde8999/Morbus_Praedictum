from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.index, name='D_index'),
    path('signup/', views.signup, name='D_signup'),
    path('login/', views.loginform, name='D_login'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='D_activate'),
    path('profile/', views.profile_page, name='D_profile'),
    path('time-slots/', views.time_slots, name='D_time_slots'),
    path('ajax/load-areas/', views.load_areas, name='D_ajax_load_areas'),
    path('edit-profile/', views.edit_profile, name='D_edit_profile'),
    path('logout/', views.user_logout, name='logout'),
]