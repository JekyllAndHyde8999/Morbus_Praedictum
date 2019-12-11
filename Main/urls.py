from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='Main_index'),
    path('login/', views.index1, name='Login_index'),
    path('signup/', views.index2, name='Signup_index'),

]