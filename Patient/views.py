from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models.functions import Concat

from .forms import *
from .tokens import account_activation_token
from .models import Address, Profile
from Doctor.models import Doctor, ClinicAddress, TimeSlots
from Corporate.models import *
from .utils import *

import datetime
import json


# Create your views here.
@login_required(login_url='P_login')
def index(request):
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user=request.user)
        return render(request, 'Patient/new_index.html', {'profile': profile})
    else:
        return redirect('/patient/profile/')


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
        return render(request, 'Patient/after_activation.html')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='P_login')
def profile_page(request):
    if request.method == 'POST':
        profile_form = UserProfileInfoForm(data=request.POST)
        address_form = AddressInfoForm(data=request.POST)
        if profile_form.is_valid() and address_form.is_valid():
            profile = profile_form.save(commit=False)
            address = address_form.save(commit=False)
            profile.user = request.user
            address.user = request.user
            profile.Patient_Email = request.user.email
            address.save()
            profile.Patient_Address = Address.objects.get(user=request.user)
            profile.save()
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
    return render(request, 'Patient/checkup.html')


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
    form = doctorSearchForm()
    if request.method == "POST":
        form = doctorSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['docName']
            city = form.cleaned_data['docCity']
            specialization = form.cleaned_data['docSpecial']
            query = name.lower().replace(" ", "")
            result = []
            if len(name) > 0:
                result = Doctor.objects.annotate(full_name=Concat('Doctor_First_Name', 'Doctor_Last_Name')
                                                 ).filter(full_name__icontains=query)
            if city:
                filtered_obj = ClinicAddress.objects.filter(city__name=city)
                r = []
                if result:
                    result = result.filter(Doctor_Address__in=filtered_obj)
                else:
                    result = Doctor.objects.filter(Doctor_Address__in=filtered_obj)
            if specialization:
                if result:
                    result = result.filter(Doctor_Specialization=specialization)
                else:
                    result = Doctor.objects.filter(Doctor_Specialization=specialization)
            searchResult = []

            if result:
                for obj in result:
                    print(obj)
                    addrs = ClinicAddress.objects.get(user=obj.user)
                    searchResult.append({"DocName": obj.Doctor_First_Name+" "+obj.Doctor_Last_Name,
                                         "Doctor_ID": obj.Doctor_ID,
                                         'Doctor_Picture': "../../media/"+str(obj.Doctor_Picture),
                                         'Doctor_Phone_Number': obj.Doctor_Phone_Number,
                                         'Doctor_Qualifications': obj.Doctor_Qualifications,
                                         'Doctor_Specialization': obj.Doctor_Specialization,
                                         'Doctor_Experience': str(obj.Doctor_Experience)+"years",
                                         'address': addrs.Home + " " + addrs.Street + "\n" + str(addrs.area) + "\n"
                                                    +str(addrs.city)})
                return render(request, 'Patient/doctorSearch.html', {'searchResult': searchResult, 'form': form})
            return render(request, 'Patient/doctorSearch.html', {'message': 'No Results Found', 'form': form})
    return render(request, 'Patient/doctorSearch.html', {'form': form})



@login_required
def doctorSearchView1(request, specialization, city):
    form = doctorSearchForm()
    filtered_obj = ClinicAddress.objects.filter(city__name=city)
    result = Doctor.objects.filter(Doctor_Address__in=filtered_obj).filter(Doctor_Specialization=specialization)

    searchResult = []
            
    if result:
        for obj in result:
            print(obj)
            addrs = ClinicAddress.objects.get(user=obj.user)
            searchResult.append({"DocName": obj.Doctor_First_Name+" "+obj.Doctor_Last_Name,
                                    "Doctor_ID": obj.Doctor_ID,
                                    'Doctor_Picture': "../../media/"+str(obj.Doctor_Picture),
                                    'Doctor_Phone_Number': obj.Doctor_Phone_Number,
                                    'Doctor_Qualifications': obj.Doctor_Qualifications,
                                    'Doctor_Specialization': obj.Doctor_Specialization,
                                    'Doctor_Experience': str(obj.Doctor_Experience)+"years",
                                    'address': addrs.Home + " " + addrs.Street + "\n" + str(addrs.area) + "\n"
                                            +str(addrs.city)})
        return render(request, 'Patient/doctorSearch1.html', {'searchResult': searchResult, 'form': form})
    return render(request, 'Patient/doctorSearch1.html', {'message': 'No Results Found', 'form': form})




@login_required(login_url='P_login')
def AppointmentBooking(request, docID):
    obj = Doctor.objects.get(Doctor_ID=docID)
    if obj:
        addrs = ClinicAddress.objects.get(user = obj.user)
        res_list = []
        date = datetime.datetime.today()
        for i in range (7):
            res_list.append(TimeSlots.objects.filter(Doctor_ID=docID, Patient_ID__isnull=True, date=date))
            date = date + datetime.timedelta(days=1)
        res_list = [i for i in res_list if i] 

        context = {"DocName": obj.Doctor_First_Name + " " + obj.Doctor_Last_Name,
                   "Doctor_ID": obj.Doctor_ID,
                   'Doctor_Picture': "../../media/" + str(obj.Doctor_Picture),
                   'Doctor_Phone_Number': obj.Doctor_Phone_Number,
                   'Doctor_Qualifications': obj.Doctor_Qualifications,
                   'Doctor_Specialization': obj.Doctor_Specialization,
                   'Doctor_Experience': str(obj.Doctor_Experience) + "years",
                   'address': addrs.Home + " " + addrs.Street + "\n" + str(addrs.area) + "\n" + str(addrs.city),
                   'slots': res_list}
        return render(request, 'Patient/appointment.html', {'context': context})


@login_required(login_url='P_login')
def confirmBooking(request):
    response_data = {}
    if request.method == "POST":
        username=request.POST['docID']
        user = User.objects.get(username=username)
        docID = Doctor.objects.get(user=user)
        print(request.user)
        date = request.POST['date']
        x = date.split(" ")
        print(date)
        opening_time = request.POST['opening_time']
        monthMap = {'Jan.': 1, 'Feb.': 2, 'Mar.': 3, 'Apr.': 4, 'May.': 5, 'Jun.': 6, 'Jul.': 7, 'Aug.': 8, 'Sep.': 9,
                    'Oct.': 10, 'Nov.': 11, 'Dec.': 12}
        str_date = (str(x[1][:-1]) + '-' + str(monthMap[x[0]]) + '-' + str(x[2]))
        corrected_date = datetime.datetime.strptime(str_date, '%d-%m-%Y')
        patient_id = Profile.objects.get(user=request.user)
        slot = TimeSlots.objects.filter(Doctor_ID=docID, date=corrected_date, Patient_ID=patient_id)
        if not slot:
            TimeSlots.objects.filter(Doctor_ID=docID, date=corrected_date,
                                     opening_Time=opening_time).update(Patient_ID=patient_id)
            response_data['success']='Booking Confirmed!'
        else:
            response_data['success'] = 'Cannot book more than 1 slot per day'
    return HttpResponse(json.dumps(response_data), content_type="application/json")



def input_symptoms(request):
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = PredictFormset(request.GET or None)
    elif request.method == 'POST':
        formset = PredictFormset(request.POST)
        print("POST REQUEST GENERATED")
        data = []
        if formset.is_valid():
            for form in formset:
                symptom = form.cleaned_data.get('name')
                data.append(symptom)
            data = [x.strip() for x in data]
            result_dict = predict(data)
            results = [[x[0], str(round(x[1] * 100, 2)) + '%'] for x in sorted(list(result_dict.items()),
                                                                               key=lambda x: -x[1])]
            # return render(request, 'Patient/predictDisease.html', {'predictions': results})
        else:
            heading_message = "Please fill form correctly"
    else:
        formset = PredictFormset(request.GET)
    return render(request, 'Patient/checkup.html', {
        'formset': formset,
        'heading': heading_message,
    })


def DiseasePredict(request):
    template_name = 'Patient/checkup.html'
    heading_message = 'Disease based on symptom'
    if request.method == 'GET':
        formset = PredictFormset(request.GET or None)
    elif request.method == 'POST':
        formset = PredictFormset(request.POST)
        if formset.is_valid():
            data = []
            for form in formset:
                name = form.cleaned_data.get('name')
                # save book instance
                if name:
                    data.append(name)
            data = [x.strip() for x in data]
            result_dict = predict(data)
            results = [[x[0], str(round(x[1] * 100, 2)) + '%'] for x in sorted(list(result_dict.items()),
                                                                               key=lambda x: -x[1])]
            # make new list of lists with list comprehension
            results = [x + [return_specialization(x[0])] for x in results if return_specialization(x[0])]
            city = Address.objects.get(user=request.user).city.name
            return render(request, 'Patient/checkup.html', {'predictions': results[:3], 'formset': formset, 'city':city})
        else:
            heading_message = "Please fill form correctly"

    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })