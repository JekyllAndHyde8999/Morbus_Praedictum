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

from .forms import SignUpForm, AddressInfoForm, UserProfileInfoForm, CustomUserEditForm
from .tokens import account_activation_token
from .models import HospitalAddress, Company
from Patient.models import Area, City

# Create your views here.
@login_required(login_url='C_login')
def index(request):
    if Company.objects.filter(user=request.user).exists():
        profile = Company.objects.get(user=request.user)
        return render(request, 'Company/index.html', {'profile': profile})
    else:
        return redirect('http://127.0.0.1:8000/company/profile')


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
            message = render_to_string('Company/emailver.html', {
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
            return render(request, 'Company/checkemail.html')
        else:
            context = {'form': form, }
            return render(request, 'Company/signup.html', context=context)
    else:
        form = SignUpForm()
        context = {'form': form, }
        return render(request, 'Company/signup.html', context=context)


def loginform(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if Company.objects.filter(user=user).exists():
                return redirect('http://127.0.0.1:8000/company')
            else:
                return redirect('http://127.0.0.1:8000/company/profile')
        else:
            print(form.errors)
            contexts = {'form': form}
            return render(request, 'Company/login.html', context=contexts)
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'Company/login.html', context=context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'Company/after_activation.html')
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
            return redirect('http://127.0.0.1:8000/company')
        elif not profile_form.is_valid():
            print(profile_form.errors)
        else:
            return render(request, 'company/profile.html',
                          {'Profile_form': profile_form, 'address_form': address_form})
    else:
        profile_form = UserProfileInfoForm()
        address_form = AddressInfoForm()
    return render(request, 'company/profile.html', {'Profile_form': profile_form, 'address_form': address_form})


def load_areas(request):
    city_id = request.GET.get('city')
    areas = Area.objects.filter(city_id=city_id).order_by('name')
    return render(request, 'company/area_dropdown_list_options.html', {'areas': areas})


@login_required(login_url='D_login')
def edit_profile(request):
    instance = Company.objects.get(user=request.user)
    form = CustomUserEditForm(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
        form.save()
        return redirect('C_index')
    return render(request, 'Company/edit_profile.html', {'Profile_form': form})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    return redirect('http://127.0.0.1:8000/')