from abc import ABC

from rest_framework import serializers
from Doctor.models import *
from Patient.models import *
from django.contrib.auth import authenticate, login
from rest_framework import exceptions


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
        fields = ('Patient_ID__Patient_Blood_Group','Patient_ID__Patient_First_Name','Patient_ID__Patient_Last_Name',
                  'Patient_ID__Patient_Phone_Number','Patient_ID__Patient_Gender','Patient_ID__Patient_DOB',
                  'Patient_ID__Patient_Email','city')


class BdSerializer(serializers.ModelSerializer):
    # Address_ID__city = serializers.CharField()
    # address = AddressSerializer(many=True)
    Patient_Address = AddressSerializer(many=False)

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ('Patient_Address', 'Patient_First_Name', 'Patient_Last_Name', 'Patient_Phone_Number', 'Patient_Gender', 'Patient_DOB', 'Patient_Blood_Group', 'Patient_Address')



class addDoctorSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    PasswordConfirmation = serializers.CharField()
    fName = serializers.CharField()
    lName = serializers.CharField()
    Gender = serializers.IntegerField()
    DateOfBirth = serializers.DateField()
    PhoneNumber = serializers.CharField()
    Qualifications = serializers.CharField()
    Specialization = serializers.CharField()
    YearsOfExperience = serializers.CharField()
    LicenseNumber = serializers.CharField()


class loginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data


x = {
    "username": "patient1251",
    "email": "narainmukul98@gmail.com",
    "password": "qwerty@123",
    "PasswordConfirmation": "qwerty@123",
    "fName": "XYZ",
    "lName": "SHARMA",
    "Gender": "1",
    "DateOfBirth": "12/11/1999",
    "PhoneNumber": "+919121391889",
    "Qualifications": "MBBS",
    "Specialization": "5",
    "YearsOfExperience": "12",
    "LicenseNumber": "AWX-4567891235"
}
