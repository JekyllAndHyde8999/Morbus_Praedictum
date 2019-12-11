from typing import List

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from itertools import chain
from .forms import *
from .tokens import account_activation_token
from .models import *
from Main.models import Blog
import datetime


def get_date(date, day):
    dayMap = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    currday = date.weekday()
    x = (dayMap[day] - currday) % 7
    return date + datetime.timedelta(days=x)


# Function to create time slots and save them in a model
def CreateTimeSlots(docID):
    ('DOC ID:'+ str(docID))
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

# start = '09:00:00'
# x = time.strptime(start, "%H:%M:%S").time()


# Create your views here.
@login_required(login_url='D_login')
def index(request):
    if Doctor.objects.filter(user=request.user).exists():
        if Doctor.objects.get(user=request.user).Doctor_Activate:
            profile = Doctor.objects.get(user=request.user)
            return render(request, 'Doctor/index.html', {'profile': profile})
        else:
            return render(request, 'Doctor/not_activated.html')
    else:
        return redirect('/doctor/profile/')

@login_required(login_url='D_login')
def createBlog(request):
    if request.method == "POST":
        print(Doctor.objects.filter(user=request.user).exists())
        if Doctor.objects.filter(user=request.user).exists():
            doc = Doctor.objects.get(user=request.user)
            blog_obj = Blog(title=request.POST['title'], user=request.user, Doctor=doc, text=request.POST['text'])
            blog_obj.save()
            # redirect to doctor/blogs
            return redirect(f'/doctor/blogs/@{doc.user.username}')
    return render(request, 'Doctor/createblog.html')


def allBlogs(request, username):
    if Doctor.objects.filter(user=User.objects.get(username=username)).exists():
        doc = Doctor.objects.get(user=User.objects.get(username=username))
        blogs = Blog.objects.filter(Doctor=doc)
        return render(request, 'Doctor/allblogs.html', context={'blogs': blogs, 'name': username})
    else:
        return render(request, 'Doctor/allblogs.html', context={'err': True, 'name': username})

def signup(request):
    if request.user.is_authenticated:
        print("Authenticated", request.user)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('Doctor/emailver.html', {
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
            return render(request, 'Doctor/checkemail.html')
        else:
            context = {'form': form, }
            return render(request, 'Doctor/signup.html', context=context)
    else:
        form = SignUpForm()
        context = {'form': form, }
        return render(request, 'Doctor/signup.html', context=context)


def loginform(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if Doctor.objects.filter(user=user).exists():
                return redirect('http://127.0.0.1:8000/doctor')
            else:
                return redirect('http://127.0.0.1:8000/doctor/profile')
        else:
            print(form.errors)
            contexts = {'form': form}
            return render(request, 'Doctor/login.html', context=contexts)
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'Doctor/login.html', context=context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'Doctor/after_activation.html')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='D_login')
def profile_page(request):
    if request.method == 'POST':
        profile_form = UserProfileInfoForm(data=request.POST)
        address_form = AddressInfoForm(data=request.POST)
        if profile_form.is_valid() and address_form.is_valid():
            profile = profile_form.save(commit=False)
            address = address_form.save(commit=False)
            profile.user = request.user
            address.user = request.user
            profile.Doctor_Email = request.user.email
            address.save()
            profile.Doctor_Address = Doctor.objects.get(user=request.user)
            profile.save()
            return redirect('http://127.0.0.1:8000/doctor')
        elif not profile_form.is_valid():
            print(profile_form.errors)
        else:
            return render(request, 'doctor/profile.html',
                          {'Profile_form': profile_form, 'address_form': address_form})
    else:
        profile_form = UserProfileInfoForm()
        address_form = AddressInfoForm()
    return render(request, 'Doctor/profile.html', {'Profile_form': profile_form, 'address_form': address_form})


def load_areas(request):
    city_id = request.GET.get('city')
    areas = Area.objects.filter(city_id=city_id).order_by('name')
    return render(request, 'Doctor/area_dropdown_list_options.html', {'areas': areas})


@login_required(login_url='D_login')
def edit_profile(request):
    instance = Doctor.objects.get(user=request.user)
    form = CustomUserEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('D_index')
    return render(request, 'Doctor/edit_profile.html', {'Profile_form': form})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    return redirect('http://127.0.0.1:8000/')

    # %L1803YvvcObmNS80ARB exd04458@bcaoo.com


@login_required(login_url='D_login')
def doctorScheduleView(request):
    form = doctorScheduleForm()
    weekDay = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    heading_message = 'Formset'
    if request.method == 'GET':
        formset = scheduleFormset(request.GET or None, initial=[{'day': weekDay[i]} for i in range(7)])
    elif request.method == 'POST':
        formset = scheduleFormset(request.POST)
        if formset.is_valid():
            doctor_obj = Doctor.objects.get(user=request.user)
            for form in formset:
                # extract name from each form and save
                day = form.cleaned_data.get('day')
                m_openTime = form.cleaned_data.get('m_openTime')
                m_closeTime = form.cleaned_data.get('m_closeTime')
                m_interval = form.cleaned_data.get('m_interval')
                e_openTime = form.cleaned_data.get('e_openTime')
                e_closeTime = form.cleaned_data.get('e_closeTime')
                e_interval = form.cleaned_data.get('e_interval')
                ("*****"+str(day)+" "+str(m_openTime)+" "+str(m_closeTime)+"*****")
                if m_openTime and m_closeTime and e_openTime and e_closeTime:
                    if m_openTime < m_closeTime and e_openTime < e_closeTime:

                        # save book instance

                        if day and doctor_obj:
                            if m_openTime and m_closeTime and m_interval:
                                doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=m_openTime,
                                               closeTime=m_closeTime, interval=m_interval).save()

                            if e_openTime and e_closeTime and e_interval:
                                doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=e_openTime,
                                               closeTime=e_closeTime, interval=e_interval).save()
            CreateTimeSlots(doctor_obj)
            return HttpResponseRedirect(request.path_info)
    return render(request, 'Doctor/scheduling.html', {
        'formset': formset,
        'heading': heading_message,
    })


@login_required(login_url='D_login')
def editDoctorSchedule(request):
    form = doctorScheduleForm()
    weekDay = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    heading_message = 'Formset'
    if request.method == 'GET':
        formset = scheduleFormset(request.GET or None, initial=[{'day': weekDay[i]} for i in range(7)])
    elif request.method == 'POST':
        formset = scheduleFormset(request.POST)
        if formset.is_valid():
            doctor_obj = Doctor.objects.get(user=request.user)
            i = 0
            for form in formset:
                # extract name from each form and save
                day = form.cleaned_data.get('day')
                m_openTime = form.cleaned_data.get('m_openTime')
                m_closeTime = form.cleaned_data.get('m_closeTime')
                m_interval = form.cleaned_data.get('m_interval')
                e_openTime = form.cleaned_data.get('e_openTime')
                e_closeTime = form.cleaned_data.get('e_closeTime')
                e_interval = form.cleaned_data.get('e_interval')
                if (m_openTime and m_closeTime) or (e_openTime and e_closeTime):
                    if m_openTime < m_closeTime and e_openTime < e_closeTime:

                        # save book instance
                        if day and doctor_obj:
                            if ((m_openTime and m_closeTime and m_interval) or (e_openTime and e_closeTime and
                                                                                e_interval)) and i == 0:
                                doctorSchedule.objects.filter(Doctor_ID=Doctor.objects.get(user=request.user)).delete()
                                i = 1
                            if m_openTime and m_closeTime and m_interval:
                                doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=m_openTime,
                                               closeTime=m_closeTime, interval=m_interval).save()

                            if e_openTime and e_closeTime and e_interval:
                                doctorSchedule(Doctor_ID=doctor_obj, day=day, openTime=e_openTime,
                                               closeTime=e_closeTime, interval=e_interval).save()
            TimeSlots.objects.filter(Doctor_ID=Doctor.objects.get(user=request.user)).delete()
            CreateTimeSlots(doctor_obj)
            return HttpResponseRedirect(request.path_info)
    return render(request, 'Doctor/editSchedule.html', {
        'formset': formset,
        'heading': heading_message,
    })


def feedBack(request):
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
