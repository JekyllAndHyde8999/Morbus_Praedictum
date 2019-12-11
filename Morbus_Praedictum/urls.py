"""Morbus_Praedictum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from miscellaneous import views as miscViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Main.urls')),
    path('patient/', include('Patient.urls')),
    path('doctor/', include('Doctor.urls')),
    path('company/', include('Corporate.urls')),
    path('feedback/', miscViews.feedbackView, name="Feedback_html"),
    path('api/', include('apis.urls')),
    path('misc/', include('miscellaneous.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)