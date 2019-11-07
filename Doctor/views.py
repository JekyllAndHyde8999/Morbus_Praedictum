from django.shortcuts import render
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

from .forms import SignUpForm, AddressInfoForm, UserProfileInfoForm, CustomUserEditForm, TimeSlotForm
from .tokens import account_activation_token
from .models import ClinicAddress, Doctor, Area

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
        return redirect('http://127.0.0.1:8000/doctor/profile')

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
        return render(request, 'Doctor/After_Activation.html')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='D_login')
def profile_page(request):
    if request.method == 'POST':
        profile_form = UserProfileInfoForm(data=request.POST)
        address_form = AddressInfoForm(data=request.POST)
        # print(form)
        if profile_form.is_valid() and address_form.is_valid():
            profile = profile_form.save(commit=False)
            address = address_form.save(commit=False)
            profile.user = request.user
            profile.Doctor_Email = request.user.email
            profile.save()
            address.Doctor_ID = Doctor.objects.get(user=request.user)
            address.save()
            return redirect('http://127.0.0.1:8000/doctor')
        elif not profile_form.is_valid():
            print(profile_form.errors)
        else:
            return render(request, 'doctor/profile.html',
                          {'Profile_form': profile_form, 'address_form': address_form})
    else:
        profile_form = UserProfileInfoForm()
        address_form = AddressInfoForm()
    return render(request, 'doctor/profile.html', {'Profile_form': profile_form, 'address_form': address_form})

def load_areas(request):
    city_id = request.GET.get('city')
    areas = Area.objects.filter(city_id=city_id).order_by('name')
    return render(request, 'Doctor/area_dropdown_list_options.html', {'areas': areas})

def time_slots(request):
    if request.method == 'POST':
        pass
    else:
        slot_form_1 = TimeSlotForm(prefix='Monday', initial={'Day':1}),
        slot_form_2 = TimeSlotForm(prefix='Tuesday', initial={'Day':2}),
        slot_form_3 = TimeSlotForm(prefix='Wednedday', initial={'Day':3}),
        slot_form_4 = TimeSlotForm(prefix='Thursday', initial={'Day':4}),
        slot_form_5 = TimeSlotForm(prefix='Friday', initial={'Day':5}),
        slot_form_6 = TimeSlotForm(prefix='Saturday', initial={'Day':6}),
        slot_form_7 = TimeSlotForm(prefix='Sunday', initial={'Day':7}),
        forms = [slot_form_1, slot_form_2, slot_form_3, slot_form_4]
        context = {
            'forms':forms
        }
        return render(request, 'Doctor/time_slots.html', context=context)

@login_required(login_url='D_login')
def edit_profile(request):
    instance = Doctor.objects.get(user=request.user)
    form = CustomUserEditForm(request.POST or None, request.FILES or None,instance=instance)
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