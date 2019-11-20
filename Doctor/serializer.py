from rest_framework import serializers
from .models import *


class scheduleSerializer(serializers.ModelSerializer):
    openTime = serializers.TimeField(input_formats=['ISO-8601'])
    closeTime = serializers.TimeField(input_formats=['ISO-8601'])

    class Meta:
        model = doctorSchedule
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'