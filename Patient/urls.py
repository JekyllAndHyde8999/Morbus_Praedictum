from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.index, name='P_index'),
    path('signup/', views.signup, name='P_signup'),
    path('login/', views.loginform, name='P_login'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='P_activate'),
    path('profile/', views.profile_page, name='P_profile'),
    path('ajax/load-areas/', views.load_areas, name='P_ajax_load_areas'),
    path('logout/', views.user_logout, name='logout'),

]