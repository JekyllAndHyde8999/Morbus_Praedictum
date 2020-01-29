from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import datetime

from .forms import *
from .tokens import account_activation_token
from .models import *
from Patient.models import *
from Doctor.forms import UserProfileInfoForm as DoctorProfileForm
# Create your views here.


def get_date(date, day):
    dayMap = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    currday = date.weekday()
    x = (dayMap[day] - currday) % 7
    return date + datetime.timedelta(days=x)


# Function to create time slots and save them in a model
def CreateTimeSlots(docID):
    print('DOC ID:'+ str(docID))
    schedule = doctorSchedule.objects.filter(Doctor_ID=docID)
    for i in schedule:
        start_time = str(i.openTime)
        end_time = str(i.closeTime)
        slot_time = i.interval
        day = i.day
        time = datetime.datetime.strptime(start_time, '%H:%M:%S')
        end = datetime.datetime.strptime(end_time, '%H:%M:%S')
        while time <= end:
            op_time = time.time()
            date = get_date(datetime.datetime.today(), day)
            TimeSlots(Doctor_ID=docID, day=day, date=date, opening_Time=op_time).save()
            time += datetime.timedelta(minutes=slot_time)


@login_required(login_url='C_login')
def index(request):
    if Company.objects.filter(user=request.user).exists():
        profile = Company.objects.get(user=request.user)
        doctors = Doctor.objects.filter(Doctor_Corporate=Company.objects.get(user=request.user))
        return render(request, 'Corporate/index_new.html', {'profile': profile, 'doctors':doctors})
    else:
        return redirect('http://192.168.43.144:8080/company/profile')


def signup(request):
    if request.user.is_authenticated:
        print("Authenticated", request.user)
    #     return redirect('192.168.43.144/patient/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('Corporate/emailver.html', {
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
            return render(request, 'Corporate/checkemail.html')
        else:
            context = {'form': form, }
            return render(request, 'Corporate/signup.html', context=context)
    else:
        form = SignUpForm()
        context = {'form': form, }
        return render(request, 'Corporate/signup.html', context=context)


def loginform(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if Company.objects.filter(user=user).exists():
                return redirect('http://192.168.43.144:8080/company')
            else:
                return redirect('http://192.168.43.144:8080/company/profile')
        else:
            contexts = {'form': form}
            return render(request, 'Corporate/login.html', context=contexts)
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'Corporate/login.html', context=context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'Corporate/after_activation.html')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='C_login')
def profile_page(request):
    if request.method == 'POST':
        profile_form = UserProfileInfoForm(data=request.POST)
        address_form = AddressInfoForm(data=request.POST)
        # print(form)
        if profile_form.is_valid() and address_form.is_valid():
            profile = profile_form.save(commit=False)
            address = address_form.save(commit=False)
            profile.user = request.user
            address.user = request.user
            profile.Patient_Email = request.user.email
            address.save()
            profile.Patient_Address = HospitalAddress.objects.get(user=request.user)
            profile.save()
            return redirect('http://192.168.43.144:8080/company')
        elif not profile_form.is_valid():
            print(profile_form.errors)
        else:
            return render(request, 'Corporate/profile.html',
                          {'Profile_form': profile_form, 'address_form': address_form})
    else:
        profile_form = UserProfileInfoForm()
        address_form = AddressInfoForm()
    return render(request, 'Corporate/profile.html', {'Profile_form': profile_form, 'address_form': address_form})


def load_areas(request):
    city_id = request.GET.get('city')
    areas = Area.objects.filter(city_id=city_id).order_by('name')
    return render(request, 'Corporate/area_dropdown_list_options.html', {'areas': areas})


@login_required(login_url='C_login')
def edit_profile(request):
    instance = Company.objects.get(user=request.user)
    form = CustomUserEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('C_index')
    return render(request, 'Corporate/edit_profile.html', {'Profile_form': form})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    return redirect('http://192.168.43.144:8080/')


@login_required(login_url='C_login')
def addDoctor(request):
    if request.method == 'POST':
        profile_form = DoctorProfileForm(data=request.POST)
        print(request.POST)
        user_form = SignUpForm(data=request.POST)

        if profile_form.is_valid() and user_form.is_valid():
            profile = profile_form.save(commit=False)
            user = user_form.save()
            profile.user = User.objects.get(username=request.POST.get("username"))
            profile.Doctor_Email = request.POST.get("email")
            profile.Doctor_Corporate = Company.objects.get(user=request.user)
            address = HospitalAddress.objects.get(user=request.user)
            c = ClinicAddress(user=User.objects.get(username=request.POST.get("username")), Home=address.Home,
                              Street=address.Street, city=address.city, area=address.area, Pin=address.Pin)
            c.save()
            profile.Doctor_Address = c
            profile.Doctor_Activate = True
            profile.save()
            return redirect('http://192.168.43.144:8080/company/')
        elif not profile_form.is_valid():
            print(profile_form.errors)
        else:
            return render(request, 'Corporate/addDoctor.html',
                          {'Profile_form': profile_form, 'address_form': user_form})
    else:
        profile_form = DoctorProfileForm()
        user_form = SignUpForm()
    return render(request, 'Corporate/addDoctor.html', {'Profile_form': profile_form, 'address_form': user_form})


def addDoctors(request):
    if request.method == 'POST':
        file1 = request.FILES.get('data')
        if not file1:
            result = 'No file uploaded.'
            # return render(request, 'predictReview/batch_predict.html', {'result' : result})
        ext = file1.name
        if (not ".txt" in ext) or(file1.content_type != 'text/plain') :
            result = 'Please upload .txt file only.'
            # return render(request, 'predictReview/batch_predict.html', {'result' : result})
        
        lst = file1.read().splitlines()
        nlist = []
        for i in lst :
            nlist.append(i.decode('utf-8').split(', '))
        
        for i in nlist:
            if len(i) != 11:
                result = "Data not in correct format."
            user = User.objects.create_user(str(i[0]), email=str(i[1]), password=str(i[2]))
            address = HospitalAddress.objects.get(user=request.user)
            c = ClinicAddress(user=User.objects.get(username=str(i[0])), Home=address.Home,
                              Street=address.Street, city=address.city, area=address.area, Pin=address.Pin)
            c.save()
            doctor = Doctor(Doctor_First_Name=str(i[3]), Doctor_Last_Name=str(i[4]), Doctor_Gender=int(i[5]),
                            Doctor_Phone_Number=str(i[6]), Doctor_Qualifications=str(i[7]),
                            Doctor_Specialization=int(i[8]), Doctor_Experience=int(i[9]), Doctor_License=str(i[10]),
                            user=user, Doctor_Corporate=Company.objects.get(user=request.user), Doctor_Address=c,
                            Doctor_Activate=True)
            doctor.save()


        print(nlist)
        
        return redirect('C_index')
    else:
        return render(request, 'Corporate/addDoctors.html')


@login_required(login_url='C_login')
def CorpDoctorScheduleView(request):
    form = CorpDoctorScheduleForm()
    weekDay = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    heading_message = 'Formset'
    if request.method == 'GET':
        formset = scheduleFormset(request.GET or None, initial=[{'day': weekDay[i]} for i in range(7)])
    elif request.method == 'POST':
        formset = scheduleFormset(request.POST)
        if formset.is_valid():
            Doctor_ID = request.POST.get('Doctor_ID')
            doctor_obj = Doctor.objects.get(Doctor_ID=Doctor_ID)
            for form in formset:
                print("inside for loop")
                # extract name from each form and save

                print("****************************")
                print(Doctor_ID)
                print("****************************")
                day = form.cleaned_data.get('day')
                m_openTime = form.cleaned_data.get('m_openTime')
                m_closeTime = form.cleaned_data.get('m_closeTime')
                m_interval = form.cleaned_data.get('m_interval')
                e_openTime = form.cleaned_data.get('e_openTime')
                e_closeTime = form.cleaned_data.get('e_closeTime')
                e_interval = form.cleaned_data.get('e_interval')
                print("@@@@@"+str(m_openTime)+" "+str(m_closeTime)+"@@@@@")
                if m_openTime and m_closeTime and e_openTime and e_closeTime:
                    if m_openTime<m_closeTime and e_openTime<e_closeTime:
                        print("&&&&&&&&&  ALL GOOD &&&&&&&&&")
                        # save book instance
                        print("$$$$$$$$$$$$$$$$$$$$$")
                        print(doctor_obj)
                        print("$$$$$$$$$$$$$$$$$$$$$")
                        if day and doctor_obj:
                            print(request.user)
                            if m_openTime and m_closeTime and m_interval:
                                doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=m_openTime, closeTime=m_closeTime,
                                               interval=m_interval).save()

                            if e_openTime and e_closeTime and e_interval:
                                doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=e_openTime, closeTime=e_closeTime,
                                               interval=e_interval).save()
            CreateTimeSlots(doctor_obj)
            return HttpResponseRedirect(request.path_info)
    return render(request, 'Corporate/addSchedule.html', {
        'formset': formset,
        'heading': heading_message,
        'DoctorListForm': corpDoctorListForm(user=request.user),
    })


@login_required(login_url='C_login')
def editCorpDoctorSchedule(request):
    form = CorpEditDoctorScheduleForm()
    weekDay = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    heading_message = 'Formset'
    if request.method == 'GET':
        formset = editScheduleFormset(request.GET or None, initial=[{'day': weekDay[i]} for i in range(7)])
    elif request.method == 'POST':
        formset = editScheduleFormset(request.POST)
        if formset.is_valid():
            Doctor_ID = request.POST.get('Doctor_ID')
            doctor_obj = Doctor.objects.get(Doctor_ID=Doctor_ID)
            i = 0
            for form in formset:

                print("inside for loop")
                # extract name from each form and save
                print("****************************")
                print(Doctor_ID)
                day = form.cleaned_data.get('day')
                m_openTime = form.cleaned_data.get('m_openTime')
                m_closeTime = form.cleaned_data.get('m_closeTime')
                m_interval = form.cleaned_data.get('m_interval')
                e_openTime = form.cleaned_data.get('e_openTime')
                e_closeTime = form.cleaned_data.get('e_closeTime')
                e_interval = form.cleaned_data.get('e_interval')
                print("*****"+str(m_openTime)+" "+str(m_closeTime)+"*****")
                if (m_openTime and m_closeTime) or (e_openTime and e_closeTime):
                    if m_openTime < m_closeTime and e_openTime < e_closeTime:
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                        # save book instance
                        if day and doctor_obj:
                            print(request.user)

                            if ((m_openTime and m_closeTime and m_interval) or (e_openTime and e_closeTime and e_interval)) and i == 0:
                                doctorSchedule.objects.filter(Doctor_ID=doctor_obj).delete()
                                i = 1
                            if m_openTime and m_closeTime and m_interval:
                                print("Doin the thing")
                                doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=m_openTime,
                                               closeTime=m_closeTime,
                                               interval=m_interval).save()

                            if e_openTime and e_closeTime and e_interval:
                                doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=e_openTime,
                                               closeTime=e_closeTime,
                                               interval=e_interval).save()
            TimeSlots.objects.filter(Doctor_ID=doctor_obj).delete()
            CreateTimeSlots(doctor_obj)
            return HttpResponseRedirect(request.path_info)
    return render(request, 'Corporate/CorpEditSchedule.html', {
        'formset': formset,
        'heading': heading_message,
        'DoctorListForm': corpDoctorListForm(user=request.user),
    })
