from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
import datetime as dt
from .models import *
from Doctor.models import *


m_HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 13)]
m_HOUR_CHOICES.insert(0, (None, 'closed'))
e_HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(12, 24)]
e_HOUR_CHOICES.insert(0, (None, 'closed'))

slotTimeChoices = (
    (10, '10 min'),
    (15, '15 min'),
    (20, '20 min'),
    (30, '30 min'),
    (60, '60 min')
)

HOURS = []


# Form for Signing Up.
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Input a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class UserProfileInfoForm(forms.ModelForm):
    Comapny_Logo = forms.ImageField(label='Logo Photo', required=False, error_messages={'invalid':"Image files only."},
                                    widget=forms.FileInput)
    
    class Meta:
        model = Company
        fields = ('Company_Name', 'Company_Logo', 'Company_Phone_Number', 'Company_License_Number')
        labels = {'Company_Name':"Name of the Organisation",
                  'Company_License_Number': 'License Number',
                  'Company_Email': 'Email ID',
                  'Company_Phone_Number': 'Phone Number',
                  'Company_Logo': 'Logo Photo'}

    def clean_avatar(self):
        avatar = self.cleaned_data['Company_Logo']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            # validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass


# Form to get user's address.
class AddressInfoForm(forms.ModelForm):
    class Meta:
        model = HospitalAddress
        fields = ('Home', 'Street', 'city', 'area', 'Pin')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()
        print(self.fields['area'].queryset)

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['area'].queryset = Area.objects.filter(
                    city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty city queryset
        # elif self.instance.pk:
        #     self.fields['area'].queryset = self.instance.city.area_set.order_by(
        #         'name')


class CustomUserEditForm(forms.ModelForm):
    Company_Logo = forms.ImageField(label='Logo Photo', required=False, error_messages = {'invalid':"Image files only."},
                                    widget=forms.FileInput)

    class Meta:
        model = Company
        fields = ('Company_Name', 'Company_Logo', 'Company_Phone_Number', 'Company_License_Number')
        labels = {'Company_Name': "Name of the Organisation",
                  'Company_License_Number': 'License Number',
                  'Company_Email': 'Email ID',
                  'Company_Phone_Number': 'Phone Number',
                  'Company_Logo': 'Logo Photo'}

    def clean_avatar(self):
        avatar = self.cleaned_data['Company_Logo']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass


class CorpDoctorScheduleForm(forms.ModelForm):

    m_interval = forms.IntegerField(widget=forms.Select(choices=slotTimeChoices), initial='10')
    m_openTime = forms.TimeField(widget=forms.Select(choices=m_HOUR_CHOICES), label="opening time", required=False)
    m_closeTime = forms.TimeField(widget=forms.Select(choices=m_HOUR_CHOICES), label="closing time", required=False)

    e_interval = forms.IntegerField(widget=forms.Select(choices=slotTimeChoices), initial='10')
    e_openTime = forms.TimeField(widget=forms.Select(choices=e_HOUR_CHOICES), label="opening time", required=False)
    e_closeTime = forms.TimeField(widget=forms.Select(choices=e_HOUR_CHOICES), label="closing time", required=False)

    def __init__(self, *args, **kwargs):
        super(CorpDoctorScheduleForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['day'].widget.attrs['readonly'] = True

    class Meta:
        model = doctorSchedule
        fields = ('day',)
        readonly_fields = ('day',)


scheduleFormset = formset_factory(CorpDoctorScheduleForm, extra=0)


class corpDoctorListForm(forms.ModelForm):
    class Meta:
        model = doctorSchedule
        fields = ('Doctor_ID',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(corpDoctorListForm, self).__init__(*args, **kwargs)

        self.fields['Doctor_ID'].queryset = Doctor.objects.filter(Doctor_Corporate=Company.objects.get(user=self.user))
        print(self.fields['Doctor_ID'].queryset)

        if 'Doctor_ID' in self.data:
            try:
                doctor_id = int(self.data.get('Doctor_ID'))
                self.fields['Doctor_ID'].queryset = Doctor.objects.none()
            except (ValueError, TypeError):
                pass


class CorpEditDoctorScheduleForm(forms.ModelForm):
    m_interval = forms.IntegerField(widget=forms.Select(choices=slotTimeChoices), initial='10')
    m_openTime = forms.TimeField(widget=forms.Select(choices=m_HOUR_CHOICES), label="opening time", required=False)
    m_closeTime = forms.TimeField(widget=forms.Select(choices=m_HOUR_CHOICES), label="closing time", required=False)

    e_interval = forms.IntegerField(widget=forms.Select(choices=slotTimeChoices), initial='10')
    e_openTime = forms.TimeField(widget=forms.Select(choices=e_HOUR_CHOICES), label="opening time", required=False)
    e_closeTime = forms.TimeField(widget=forms.Select(choices=e_HOUR_CHOICES), label="closing time", required=False )

    def __init__(self, *args, **kwargs):
        super(CorpEditDoctorScheduleForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['day'].widget.attrs['readonly'] = True

    class Meta:
        model = doctorSchedule
        fields = ('day',)
        readonly_fields = ('day',)


editScheduleFormset = formset_factory(CorpEditDoctorScheduleForm, extra=0)
