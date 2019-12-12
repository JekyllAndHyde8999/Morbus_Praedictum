from Patient.utils import *
from .serializer import *


from rest_framework import filters, generics, status, views
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
import datetime
from Corporate.forms import *
from Doctor.views import CreateTimeSlots
from Main.models import *

bloodGroupMap = {
    "A+": 1,
    "A-": 2,
    "B+": 3,
    "B-": 4,
    "AB+": 5,
    "AB-": 6,
    "O+": 7,
    "O-": 8,
}


# Create your views here.
class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


class viewDoctorScheduleApiView(views.APIView):
    def get(self, request):
        user = request.user
        doctor_obj = Doctor.objects.get(user=user)
        queryset = doctorSchedule.objects.filter(Doctor_ID=doctor_obj)
        serializer = scheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class addDoctorScheduleApiView(views.APIView):
    def post(self, request):
        user = request.user
        doctor_obj = Doctor.objects.get(user=user)
        data = request.data
        print(data)
        day = data['day']
        m_interval = data['m_interval']
        m_openTime = datetime.datetime.strptime(data['m_openTime'], '%H:%M').time()
        m_closeTime = datetime.datetime.strptime(data['m_closeTime'], '%H:%M').time()
        e_interval = data['e_interval']
        e_openTime = datetime.datetime.strptime(data['e_openTime'], '%H:%M').time()
        e_closeTime = datetime.datetime.strptime(data['e_closeTime'], '%H:%M').time()
        if m_openTime and m_closeTime and e_openTime and e_closeTime:
            if m_openTime < m_closeTime and e_openTime < e_closeTime:

                # save book instance

                if day and doctor_obj:
                    if m_openTime and m_closeTime and m_interval:
                        doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=m_openTime,
                                       closeTime=m_closeTime, interval=int(m_interval)).save()

                    if e_openTime and e_closeTime and e_interval:
                        doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=e_openTime,
                                       closeTime=e_closeTime, interval=int(e_interval)).save()
        CreateTimeSlots(doctor_obj)
        return Response({"success": "Timeslots Added"})

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class timeSlotsApiView(views.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if str(user) != "AnonymousUser":
            docID = Doctor.objects.get(user=user)
            try:
                ts = TimeSlots.objects.get(Doctor_ID=docID)
            except:
                return Response('{Response:"No data"}')
            ts_list = list(ts)
            serializer = TimeSlotsSerializer
            return Response(serializer.data)
        return Response('{Response:"Please login first"}')

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class DoctorApi(generics.ListCreateAPIView):
    search_fields = ['Doctor_Gender', 'Doctor_Qualifications', 'Doctor_Specialization']
    filter_backends = (DynamicSearchFilter,)
    queryset = Doctor.objects.filter()
    serializer_class = DoctorSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]


# #PATIENT APIS
class BloodDonor(views.APIView):
    def get(self, request, *args, **kwargs):
        result =[]
        selected = []
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        CITY = self.request.query_params.get('city')
        BLOOD_GROUP = self.request.query_params.get('blood_group')
        print(CITY)
        print(BLOOD_GROUP)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("***************************")
        if CITY or BLOOD_GROUP:
            print("OK")
            if CITY:
                cityDB = City.objects.all()
                city_check = 0
                for city in cityDB:
                    if CITY.lower() == city.name.lower():
                        city_check = 1
                if city_check:
                    ct_id = City.objects.get(name=CITY.capitalize()).id
                    all_address = Address.objects.filter(city=ct_id)
                    for address in all_address:
                        if BLOOD_GROUP:
                            userObj = Profile.objects.get(user=address.user, Patient_Blood_Group=BLOOD_GROUP)
                        else:
                            userObj = Profile.objects.get(user=address.user)
                        selected.append(userObj.Patient_ID)
                        result.append({
                            'Patient_first_name': userObj.Patient_First_Name,
                            'Patient_last_name': userObj.Patient_Last_Name,
                            'Patient_Phone_Number': str(userObj.Patient_Phone_Number),
                            'Patient_Blood_Group': userObj.Patient_Blood_Group,
                            'Patient_City': CITY
                        })
                else:
                    return Response({})
            elif BLOOD_GROUP:
                print(BLOOD_GROUP)
                bloodGrp_id = bloodGroupMap[BLOOD_GROUP]
                bloodGrp_sorted = Profile.objects.filter(Patient_Blood_Donation=0, Patient_Blood_Group=bloodGrp_id)
                for patient in bloodGrp_sorted:
                        address = Address.objects.get(user=patient.user)
                        result.append({
                            'Patient_first_name': patient.Patient_First_Name,
                            'Patient_last_name': patient.Patient_Last_Name,
                            'Patient_Phone_Number': str(patient.Patient_Phone_Number),
                            'Patient_Blood_Group': patient.Patient_Blood_Group,
                            'Patient_City': address.city.name
                        })
            if (CITY or BLOOD_GROUP) and not result:
                return Response({"error": "No query"}, status=status.HTTP_404_NOT_FOUND)
        else:
            print("+++++++++++++++++++++++++++++++++++++++")
            bloodGrp_sorted = Profile.objects.filter(Patient_Blood_Donation=0)
            for patient in bloodGrp_sorted:
                address = Address.objects.get(user=patient.user)
                result.append({
                    'Patient_first_name': patient.Patient_First_Name,
                    'Patient_last_name': patient.Patient_Last_Name,
                    'Patient_Phone_Number': str(patient.Patient_Phone_Number),
                    'Patient_Blood_Group': patient.Patient_Blood_Group,
                    'Patient_City': address.city.name
                })
        print(result)
        return Response(result)


class BloodDonorList(generics.ListCreateAPIView):
    search_fields = ['Patient_Blood_Group']
    filter_backends = (DynamicSearchFilter,)
    queryset = Profile.objects.filter(Patient_Blood_Donation=0)
    serializer_class = BdSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]


class EyeDonorList(views.APIView):
    def get(self, request):
        queryset = EyeDonor.objects.all()
        serializer = EyeDonorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        Name_of_Donor = data['Name_of_Donor']
        time_of_death = data['time_of_death']
        attendee_name = data['attendee_name']
        contact_info = data['contact_info']
        city = data['City'].lower()
        if Name_of_Donor and time_of_death and attendee_name and contact_info and city:
            donor = EyeDonor(Name_of_Donor=Name_of_Donor, time_of_death=time_of_death,
                             attendee_name=attendee_name, contact_info=contact_info, City=city)
            donor.save()
        else:
            return Response({"error": "Enter all fields"})


class OrganDonorList(views.APIView):
    def get(self, request):
        queryset = OrganDonor.objects.all()
        serializer = OrganDonorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("POST WORKING")
        data = request.data
        Name_of_Donor = data['Name_of_Donor']
        attendee_name = data['attendee_name']
        contact_info = data['contact_info']
        city = data['City'].lower()
        if Name_of_Donor and attendee_name and contact_info and city:
            donor = OrganDonor(Name_of_Donor=Name_of_Donor, attendee_name=attendee_name, contact_info=contact_info,
                               City=city)
            donor.save()
            print("Donor Saved")
            return Response({"success": "Entry Saved"})
        else:
            return Response({"error": "Enter all fields"})


class DiseasePredictor(views.APIView):
    def get(self, request):
        raw_data = request.data
        print(request.data)
        data = raw_data['data'].split(",")
        data = [x.strip() for x in data]
        result_dict = predict(data)
        print(result_dict)
        results = [[x[0], str(round(x[1] * 100, 2)) + '%'] for x in
                   sorted(list(result_dict.items()), key=lambda x: -x[1])]
        return Response(dict(results), status=status.HTTP_200_OK)

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


# Corporate APIs
class addDoctorView(views.APIView):
    def post(self, request):

        data = request.data
        print(data)
        username = data['username']
        email = data['email']
        password1 = data['password1']
        password2 = data['password2']
        Doctor_First_Name = data['Doctor_First_Name']
        Doctor_Last_Name = data['Doctor_Last_Name']
        Doctor_Gender = data['Doctor_Gender']
        Doctor_DOB = data['Doctor_DOB']
        Doctor_Phone_Number = data['Doctor_Phone_Number']
        Doctor_Qualifications = data['Doctor_Qualifications']
        Doctor_Specialization = data['Doctor_Specialization']
        Doctor_Experience = data['Doctor_Experience']
        Doctor_License = data['Doctor_License']
        if username and email and password1 and password2 and Doctor_First_Name and Doctor_Last_Name and Doctor_Gender \
                and Doctor_DOB and Doctor_Phone_Number and Doctor_Qualifications and Doctor_Specialization and \
                Doctor_Experience and Doctor_License:
            user = User.objects.create_user(username=username, email=email, password=password1)
            address = HospitalAddress.objects.get(user=request.user)
            c = ClinicAddress(user=User.objects.get(username=str(username)), Home=address.Home,
                              Street=address.Street, city=address.city, area=address.area, Pin=address.Pin)
            c.save()
            doctor = Doctor(Doctor_First_Name=Doctor_First_Name, Doctor_Last_Name=Doctor_Last_Name,
                            Doctor_Gender=int(Doctor_Gender), Doctor_Phone_Number=str(Doctor_Phone_Number),
                            Doctor_Qualifications=str(Doctor_Qualifications),
                            Doctor_Specialization=int(Doctor_Specialization),
                            Doctor_Experience=int(Doctor_Experience), Doctor_License=str(Doctor_License),
                            user=user, Doctor_Corporate=Company.objects.get(user=request.user), Doctor_Address=c,
                            Doctor_Activate=True)
            doctor.save()
            return Response({'success': "USer added"}, status=201)
        else:
            return Response({'error': "Error occurred"}, status=201)
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class viewCorpDoctorScheduleApiView(views.APIView):
    def get(self, request):
        user = request.user
        corp_obj = Company.objects.get(user=user)
        data = request.data
        doc_user = User.objects.get(username=data['username'])
        doctor_obj = Doctor.objects.get(user=doc_user)
        queryset = doctorSchedule.objects.filter(Doctor_ID=doctor_obj)
        serializer = scheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class addCorpDoctorScheduleApiView(views.APIView):
    def post(self, request):
        user = request.user
        corp_obj = Company.objects.get(user=user)
        data = request.data
        print(data)
        doctor_user = User.objects.get(username=data['username'])
        doctor_obj = Doctor.objects.get(user=doctor_user)
        day = data['day']
        m_interval = data['m_interval']
        m_openTime = datetime.datetime.strptime(data['m_openTime'], '%H:%M').time()
        m_closeTime = datetime.datetime.strptime(data['m_closeTime'], '%H:%M').time()
        e_interval = data['e_interval']
        e_openTime = datetime.datetime.strptime(data['e_openTime'], '%H:%M').time()
        e_closeTime = datetime.datetime.strptime(data['e_closeTime'], '%H:%M').time()
        if m_openTime and m_closeTime and e_openTime and e_closeTime:
            if m_openTime < m_closeTime and e_openTime < e_closeTime:

                # save book instance

                if day and doctor_obj:
                    if m_openTime and m_closeTime and m_interval:
                        doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=m_openTime,
                                       closeTime=m_closeTime, interval=int(m_interval)).save()

                    if e_openTime and e_closeTime and e_interval:
                        doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=e_openTime,
                                       closeTime=e_closeTime, interval=int(e_interval)).save()
        CreateTimeSlots(doctor_obj)
        return Response({"success": "Timeslots Added"})

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


# General APIS
class loginViewAPI(APIView):
    def post(self, request):
        serializer = loginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class logoutViewAPI(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        django_logout(request)
        return Response(status=204)


class BlogAPI(views.APIView):
    def get(self, request):
        queryset = Blog.objects.all()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)