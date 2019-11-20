from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import F
from django.forms.models import model_to_dict

from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as filter

from rest_framework import filters, generics, status, views

from .serializer import BloodDonorSerializer, BdSerializer

from .forms import SignUpForm, AddressInfoForm, UserProfileInfoForm, CustomUserEditForm, doctorSearchForm
from .tokens import account_activation_token
from .models import Address, Profile, Area
from Doctor.models import Doctor, ClinicAddress,TimeSlots
from Patient.models import City
from .utils import *

import datetime
import json

from .utils import *

# Create your views here.
@login_required(login_url='P_login')
def index(request):
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user=request.user)
        return render(request, 'Patient/index.html', {'profile': profile})
    else:
        return redirect('http://127.0.0.1:8000/patient/profile')


def signup(request):
    if request.user.is_authenticated:
        print("Authenticated", request.user)
    #     return redirect('127.0.0.1/patient/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('Patient/emailver.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'Patient/checkemail.html')
        else:
            context = {'form': form, }
            return render(request, 'Patient/signup.html', context=context)
    else:
        form = SignUpForm()
        context = {'form': form, }
        return render(request, 'Patient/signup.html', context=context)


def loginform(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if Profile.objects.filter(user=user).exists():
                return redirect('http://127.0.0.1:8000/patient')
            else:
                return redirect('http://127.0.0.1:8000/patient/profile')
        else:
            print(form.errors)
            contexts = {'form': form}
            return render(request, 'Patient/login.html', context=contexts)
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'Patient/login.html', context=context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'Patient/After_Activation.html')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='P_login')
def profile_page(request):
    if request.method == 'POST':
        profile_form = UserProfileInfoForm(data=request.POST)
        address_form = AddressInfoForm(data=request.POST)
        # print(form)
        if profile_form.is_valid() and address_form.is_valid():
            profile = profile_form.save(commit=False)
            address = address_form.save(commit=False)
            profile.user = request.user
            profile.Patient_Email = request.user.email
            profile.save()
            address.Patient_ID = Profile.objects.get(user=request.user)
            address.save()
            return redirect('http://127.0.0.1:8000/patient')
        elif not profile_form.is_valid():
            print(profile_form.errors)
        else:
            return render(request, 'patient/profile.html',
                          {'Profile_form': profile_form, 'address_form': address_form})
    else:
        profile_form = UserProfileInfoForm()
        address_form = AddressInfoForm()
    return render(request, 'patient/profile.html', {'Profile_form': profile_form, 'address_form': address_form})


def load_areas(request):
    city_id = request.GET.get('city')
    areas = Area.objects.filter(city_id=city_id).order_by('name')
    return render(request, 'Patient/area_dropdown_list_options.html', {'areas': areas})


@login_required(login_url='P_login')
def symptoms(request):
    return render(request, 'Patient/symptoms.html')


@login_required(login_url='P_login')
def edit_profile(request):
    instance = Profile.objects.get(user=request.user)
    form = CustomUserEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('P_index')
    return render(request, 'Patient/edit_profile.html', {'Profile_form': form})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    return redirect('http://127.0.0.1:8000/')


@login_required
def doctorSearchView(request):
    # # result = Doctor.objects.get(Doctor_First_Name='John').clinicaddress_set.all()
    # #result = ClinicAddress.objects.filter(city=City.objects.get(name="Chennai"))
    # main_result = []
    # for i in result:
    #     print(i.Doctor_ID)
    #     # Doctor.objects.get(Doctor_ID=i.Doctor_ID)
    # print(main_result)

    form = doctorSearchForm()
    if request.method == "POST":
        form = doctorSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['docName']
            city = form.cleaned_data['docCity']
            specialization = form.cleaned_data['docSpecial']
            query = name.lower().replace(" ", "")
            result=[]
            if len(name) > 0:
                result = Doctor.objects.annotate(full_name=Concat('Doctor_First_Name', 'Doctor_Last_Name')
                                                 ).filter(full_name__icontains=query)
            if city:
                filtered_obj = ClinicAddress.objects.filter(city__name=city)
                if result:
                    result = result.filter(Doctor_ID__in=filtered_obj)
                else:
                    result = Doctor.objects.filter(Doctor_ID__in=filtered_obj)
            if specialization:
                if result:
                    result = result.filter(Doctor_Specialization=specialization)
                else:
                    result = Doctor.objects.filter(Doctor_Specialization=specialization)
            searchResult = []

            if result:
                for obj in result:
                    addrs = ClinicAddress.objects.get(Doctor_ID=obj.Doctor_ID)
                    searchResult.append({"DocName": obj.Doctor_First_Name+" "+obj.Doctor_Last_Name,
                                         "Doctor_ID": obj.Doctor_ID,
                                         'Doctor_Picture': "../../media/"+str( obj.Doctor_Picture),
                                         'Doctor_Phone_Number': obj.Doctor_Phone_Number,
                                         'Doctor_Qualifications': obj.Doctor_Qualifications,
                                         'Doctor_Specialization': obj.Doctor_Specialization,
                                         'Doctor_Experience': str(obj.Doctor_Experience)+"years",
                                         'address':addrs.Home + " " + addrs.Street + "\n" + str(addrs.area) + "\n" + str(addrs.city)})
                return render(request, 'Patient/searchDoctor.html', {'searchResult': searchResult,'form':form})
            return render(request, 'Patient/searchDoctor.html', {'message': 'No Results Found', 'form': form})
    return render(request, 'Patient/searchDoctor.html', {'form': form})


# class DonorList(APIView):
#
#     def get(self, request):
#         search_fields = ['Patient_First_Name']
#         filter_backends = (filters.SearchFilter,)
#         queryset = Profile.objects.all()
#         serializer = BloodDonorSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self):
#         pass

class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        print(request.GET.getlist('search_fields', []))
        return request.GET.getlist('search_fields', [])
#
#
# class DonorList(generics.ListCreateAPIView):
#     search_fields = ['Patient_ID__Patient_Blood_Group', 'Patient_ID__Patient_First_Name', 'Patient_ID__Patient_Last_Name', 'Patient_ID__Patient_Phone_Number', 'Patient_ID__Patient_Gender', 'Patient_ID__Patient_DOB', 'Patient_ID__Patient_Email', 'city']
#     filter_backends = (DynamicSearchFilter,)
#     # queryset = model_to_dict(Address.objects.select_related('Patient_ID').all().values('Patient_ID__Patient_Blood_Group','Patient_ID__Patient_First_Name', 'Patient_ID__Patient_Last_Name', 'Patient_ID__Patient_Phone_Number', 'Patient_ID__Patient_Gender','Patient_ID__Patient_DOB', 'Patient_ID__Patient_Email'))
#     # queryset = Address.objects.raw('SELECT * FROM Patient_Address INNER JOIN Patient_Profile on Patient_Address.Patient_ID_id=Patient_Profile.Patient_ID')
#     data = Address.objects.select_related('Patient_ID').all().values('Patient_ID__Patient_Blood_Group','Patient_ID__Patient_First_Name', 'Patient_ID__Patient_Last_Name', 'Patient_ID__Patient_Phone_Number', 'Patient_ID__Patient_Gender', 'Patient_ID__Patient_DOB', 'Patient_ID__Patient_Email', 'city').annotate(city=Address.objects.get(city=city))
#     print(data)
#     queryset = []
#     for query in data:
#         queryset.append({
#
#             'Patient_ID__Patient_Blood_Group':query['Patient_ID__Patient_Blood_Group'],
#             'Patient_ID__Patient_First_Name': query['Patient_ID__Patient_First_Name'],
#             'Patient_ID__Patient_Last_Name': query['Patient_ID__Patient_Last_Name'],
#             'Patient_ID__Patient_Phone_Number': query['Patient_ID__Patient_Phone_Number'],
#             'Patient_ID__Patient_Gender': query['Patient_ID__Patient_Gender'],
#             'Patient_ID__Patient_DOB': query['Patient_ID__Patient_DOB'],
#             'Patient_ID__Patient_Email': query['Patient_ID__Patient_Email'],
#             'city': City.objects.get(id=query['city']).name,
#         })
#     serializer_class = BloodDonorSerializer

# How to make above api work
# http://127.0.0.1:8000/patient/patientapi/?search=4&search_fields=Patient_Blood_Group


class DonorList(generics.ListCreateAPIView):
    search_fields = ['Patient_Blood_Group']
    filter_backends = (DynamicSearchFilter,)
    queryset = Profile.objects.filter(Patient_Blood_Donation=0)
    serializer_class = BdSerializer


@login_required(login_url='P_login')
def AppointmentBooking(request, docID):
    obj = Doctor.objects.get(Doctor_ID=docID)
    if obj:
        addrs = ClinicAddress.objects.get(Doctor_ID=docID)
        res_list = []
        date = datetime.datetime.today()
        for i in range (7):
            res_list.append(TimeSlots.objects.filter(Doctor_ID=docID, Patient_ID__isnull=True, date=date))
            date = date + datetime.timedelta(days=1)

        context = {"DocName": obj.Doctor_First_Name + " " + obj.Doctor_Last_Name,
                         "Doctor_ID": obj.Doctor_ID,
                         'Doctor_Picture': "../../media/" + str(obj.Doctor_Picture),
                         'Doctor_Phone_Number': obj.Doctor_Phone_Number,
                         'Doctor_Qualifications': obj.Doctor_Qualifications,
                         'Doctor_Specialization': obj.Doctor_Specialization,
                         'Doctor_Experience': str(obj.Doctor_Experience) + "years",
                         'address': addrs.Home + " " + addrs.Street + "\n" + str(addrs.area) + "\n" + str(addrs.city),
                         'slots':res_list}
        return render(request, 'Patient/appointment_Booking.html', {'context': context})


# @login_required(login_url='P_login')
# def confirmBooking(request):
#     response_data = {}
#     if request.method == "POST":
#         username=request.POST['docID']
#         user = User.objects.get(username=username)
#         docID = Doctor.objects.get(user=user)
#         print(request.user)
#         date = request.POST['date']
#         x = date.split(" ")
#         print(date)
#         opening_time = request.POST['opening_time']
#         monthMap = {'Jan.': 1, 'Feb.': 2, 'Mar.': 3, 'Apr.': 4, 'May.': 5, 'Jun.': 6, 'Jul.': 7, 'Aug.': 8, 'Sep.': 9,
#                     'Oct.': 10, 'Nov.': 11, 'Dec.': 12}
#         str_date = (str(x[1][:-1]) + '-' + str(monthMap[x[0]]) + '-' + str(x[2]))
#         corrected_date = datetime.datetime.strptime(str_date, '%d-%m-%Y')
#         patient_id = Profile.objects.get(user=request.user)
#         slot = TimeSlots.objects.filter(Doctor_ID=docID, date=corrected_date, Patient_ID=patient_id)
#         if not slot:
#             TimeSlots.objects.filter(Doctor_ID=docID, date=corrected_date, opening_Time=opening_time).update(Patient_ID=patient_id)
#             response_data['success']='Booking Confirmed!'
#         else:
#             response_data['success'] = 'Cannot book more than 1 slot per day'
#     return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='P_login')
def confirmBooking(request):
    response_data = {}
    if request.method == "POST":
        retVariable = request.POST['docID']
        res_list = retVariable.split(", ")
        user = User.objects.get(username=res_list[0])
        docID = Doctor.objects.get(user=user)
        # date = request.POST['date']
        # opening_time = request.POST['opening_time']
        patient_id = Profile.objects.get(user=request.user)
        slot = TimeSlots.objects.filter(Doctor_ID=docID, date=res_list[1], Patient_ID=patient_id)
        if not slot:
            TimeSlots.objects.filter(Doctor_ID=docID, date=res_list[1], opening_Time=res_list[2]).update(Patient_ID=patient_id)
            response_data['success'] = 'Booking Confirmed!'
        else:
            response_data['success'] = 'Cannot book more than 1 slot per day'
    return HttpResponse(json.dumps(response_data), content_type="application/json")



def input_symptoms(request):
    if request.method == 'POST':
        raw_data = request.POST['inputs']
        data = raw_data.split(",")
        data = [x.strip() for x in data]
        result_dict = predict(data)
        print(result_dict)
        results = [[x[0], str(round(x[1] * 100, 2)) + '%'] for x in sorted(list(result_dict.items()), key=lambda x: -x[1])]
        return render(request, 'Patient/predictDisease.html', {'predictions': results})
    return render(request, 'Patient/predictDisease.html')


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