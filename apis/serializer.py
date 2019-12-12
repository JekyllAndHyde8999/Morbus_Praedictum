from rest_framework import serializers
from Doctor.models import *
from Patient.models import *
from Main.models import EyeDonor, OrganDonor, Blog
from django.contrib.auth import authenticate
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
        fields = ('Patient_ID__Patient_Blood_Group', 'Patient_ID__Patient_First_Name', 'Patient_ID__Patient_Last_Name',
                  'Patient_ID__Patient_Phone_Number', 'Patient_ID__Patient_Gender', 'Patient_ID__Patient_DOB',
                  'Patient_ID__Patient_Email', 'city')


class EyeDonorSerializer(serializers.ModelSerializer):
    time_of_death = serializers.TimeField(input_formats=['ISO-8601'])

    class Meta:
        model = EyeDonor
        fields = ('Name_of_Donor', 'time_of_death', 'attendee_name', 'contact_info', 'City')


class OrganDonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganDonor
        fields = ('Name_of_Donor', 'attendee_name', 'contact_info', 'City')


class BdSerializer(serializers.ModelSerializer):
    # Address_ID__city = serializers.CharField()
    # address = AddressSerializer(many=True)
    Patient_Address = AddressSerializer(many=False)

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ('Patient_Address', 'Patient_First_Name', 'Patient_Last_Name', 'Patient_Phone_Number',
                  'Patient_Gender', 'Patient_DOB', 'Patient_Blood_Group', 'Patient_Address')


class addDoctorSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    Doctor_First_Name = serializers.CharField()
    Doctor_Last_Name = serializers.CharField()
    Doctor_Gender = serializers.IntegerField()
    Doctor_DOB = serializers.DateField()
    Doctor_Phone_Number = serializers.CharField()
    Doctor_Qualifications = serializers.CharField()
    Doctor_Specialization = serializers.CharField()
    Doctor_Experience = serializers.CharField()
    Doctor_License = serializers.CharField()


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


class BlogSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['ISO-8601'])
    class Meta:
        model = Blog
        fields = ('Doctor', 'title', 'text', 'date')


# trial json(POST) for addDoctor(corporate) API
x = {
    "username": "doctor45656",
    "email": "narainmukul98@gmail.com",
    "password1": "qwerty@123",
    "password2": "qwerty@123",
    "Doctor_First_Name": "XYZ",
    "Doctor_Last_Name": "SHARMA",
    "Doctor_Gender": "1",
    "Doctor_DOB": "12/11/1999",
    "Doctor_Phone_Number": "+919121391889",
    "Doctor_Qualifications": "MBBS",
    "Doctor_Specialization": "5",
    "Doctor_Experience": "12",
    "Doctor_License": "AWX-4567891235"
}


# trial json(POST) for addSchedule(Doctor) API
y = {
    "day": "Thursday",
    "m_interval": "60",
    "m_openTime": "07:00",
    "m_closeTime": "12:00",
    "e_interval": "60",
    "e_openTime": "14:00",
    "e_closeTime": "19:00"
}

# trial json(POST) for CorpAddSchedule(Doctor) API
z = {
    "username": "jh",
    "day": "Thursday",
    "m_interval": "60",
    "m_openTime": "07:00",
    "m_closeTime": "12:00",
    "e_interval": "60",
    "e_openTime": "14:00",
    "e_closeTime": "19:00"
}

w = {
    "Name_of_Donor": "Mukesh Sharma",
    "attendee_name": "Sukesh Sharma",
    "contact_info": "+918528528525",
    "City": "Jaipur"
}

v = {
    "Name_of_Donor": "Mukesh Sharma",
    "attendee_name": "Sukesh Sharma",
    "contact_info": "+918528528525",
    "City": "Jaipur"
}