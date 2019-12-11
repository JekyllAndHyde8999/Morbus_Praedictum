from django.urls import path
from . import views

urlpatterns = [
    path('feedback', views.feedbackView, name="feedback")
    ]