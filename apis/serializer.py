from rest_framework import serializers
from Doctor.models import *
from Patient.models import *


# #DOCTOR APIS
class scheduleSerializer(serializers.ModelSerializer):
    openTime = serializers.TimeField(input_formats=['ISO-8601'])
    closeTime = serializers.TimeField(input_formats=['ISO-8601'])

    class Meta:
        model = doctorSchedule
        fields = '__all__'


class TimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


# #PATIENT APIS
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class BloodDonorSerializer(serializers.ModelSerializer):
    # City = serializers.SerializerMethodField(city)
    # address = AddressSerializer(many=True)
    Patient_ID__Patient_Blood_Group = serializers.IntegerField()
    Patient_ID__Patient_First_Name = serializers.CharField()
    Patient_ID__Patient_Last_Name = serializers.CharField()
    Patient_ID__Patient_Phone_Number = serializers.CharField()
    Patient_ID__Patient_Gender = serializers.IntegerField()
    Patient_ID__Patient_DOB = serializers.DateField()
    Patient_ID__Patient_Email = serializers.EmailField()
    city = serializers.CharField()

    class Meta:
        model = Address
        fields = ('Patient_ID__Patient_Blood_Group','Patient_ID__Patient_First_Name','Patient_ID__Patient_Last_Name','Patient_ID__Patient_Phone_Number','Patient_ID__Patient_Gender','Patient_ID__Patient_DOB','Patient_ID__Patient_Email','city')


class BdSerializer(serializers.ModelSerializer):
    # Address_ID__city = serializers.CharField()
    # address = AddressSerializer(many=True)
    Patient_Address = AddressSerializer(many=False)

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ('Patient_Address', 'Patient_First_Name', 'Patient_Last_Name', 'Patient_Phone_Number', 'Patient_Gender', 'Patient_DOB', 'Patient_Blood_Group', 'Patient_Address')
