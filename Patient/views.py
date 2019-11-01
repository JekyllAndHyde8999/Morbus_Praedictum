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


from .forms import SignUpForm, AddressInfoForm, UserProfileInfoForm
from .tokens import account_activation_token
from .models import Address, Profile, Area


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

def symptoms(request):
    return render(request, 'Patient/symptoms.html')

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    return redirect('http://127.0.0.1:8000/')
