
from Doctor.models import *
from Patient.models import *
from Patient.utils import *
from .serializer import *

from django.http import JsonResponse

from rest_framework import filters, generics, status, views
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser

# Create your views here.
class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


class scheduleApiView(generics.ListCreateAPIView):
    search_fields = ['Doctor_ID']
    filter_backends = (DynamicSearchFilter,)
    queryset = doctorSchedule.objects.filter()
    serializer_class = scheduleSerializer
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
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


# #PATIENT APIS


class DonorList(generics.ListCreateAPIView):
    search_fields = ['Patient_Blood_Group']
    filter_backends = (DynamicSearchFilter,)
    queryset = Profile.objects.filter(Patient_Blood_Donation=0)
    serializer_class = BdSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class DiseasePredictor(views.APIView):
    def post(self, request):
        raw_data = request.data
        data = raw_data['data'].split(",")
        data = [x.strip() for x in data]
        result_dict = predict(data)
        print(result_dict)
        results = [[x[0], str(round(x[1] * 100, 2)) + '%'] for x in
                   sorted(list(result_dict.items()), key=lambda x: -x[1])]
        return Response(result_dict, status=status.HTTP_200_OK)

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


# Corporate APIs
class addDoctorView(views.APIView):
    print("************************")
    def post(self, request):
        data = request.data
        print(data)
        username = data['username']
        email = data['email']
        password = data['password']
        PasswordConfirmation = data['PasswordConfirmation']
        fName = data['fName']
        lName = data['lName']
        Gender = data['Gender']
        DateOfBirth = data['DateOfBirth']
        PhoneNumber = data['PhoneNumber']
        Qualifications = data['Qualifications']
        Specialization = data['Specialization']
        YearsOfExperience = data['YearsOfExperience']
        LicenseNumber = data['LicenseNumber']
        if username and email and password and PasswordConfirmation and fName and lName and Gender and DateOfBirth\
                and PhoneNumber and Qualifications and Specialization and YearsOfExperience and LicenseNumber:

            return Response({'success': "Now proceed"}, status=201)
        else:
            return Response({'error': "Enter all fields"}, status=201)
        # return Response({}, status=201)


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

