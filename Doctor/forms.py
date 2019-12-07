from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from .models import ClinicAddress, Area, Doctor, doctorSchedule

import datetime as dt
from django.forms import formset_factory

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


class DateInput(forms.DateInput):
    input_type = 'date'


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = Doctor
        widgets = {
            'Doctor_DOB': DateInput()
        }
        fields = ('Doctor_First_Name', 'Doctor_Last_Name', 'Doctor_Gender', 'Doctor_Picture', 'Doctor_DOB', 'Doctor_Phone_Number', 'Doctor_Qualifications', 'Doctor_Specialization', 'Doctor_Experience')
        labels = {'Doctor_First_Name': "First Name",
                  'Doctor_Last_Name': "Last Name",
                  'Doctor_Gender': "Gender",
                  'Doctor_DOB': 'Date of Birth',
                  'Doctor_Phone_Number': 'Phone Number',
                  'Doctor_Picture':'Picture',
                  'Doctor_Qualifications': 'Qualifications',
                  'Doctor_Specialization': 'Specialization',
                  'Doctor_Experience': 'Years of Experience',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data['Doctor_Picture']

        try:
            w, h = get_image_dimensions(avatar)

            # #validate dimensions
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


class AddressInfoForm(forms.ModelForm):
    class Meta:
        model = ClinicAddress
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
        #     print(self.instance.pk)
        #     self.fields['area'].queryset = self.instance.city.area_set.order_by(
        #         'name')


# class TimeSlotForm(forms.ModelForm):
#     class Meta:
#         widgets = {
#             'Opening_Time':TimePicker(
#             attrs={
#                 'input_toggle': True,
#                 'input_group': True,
#             },),
#             'Closing_Time':forms.TimeInput(format='%I:%M %p')
#         }
#         model = TimeSlots
#         fields = {'Day', 'openingTime', 'Closing_Time', 'Interval'}


class CustomUserEditForm(forms.ModelForm):
    Doctor_Picture = forms.ImageField(label='Picture', required=False, error_messages = {'invalid':"Image files only."},
                                      widget=forms.FileInput)
    
    class Meta:
        widgets = {
            'Doctor_DOB': DateInput()
        }
        model = Doctor
        fields = ('Doctor_First_Name', 'Doctor_Last_Name', 'Doctor_Gender', 'Doctor_Picture', 'Doctor_DOB',
                  'Doctor_Phone_Number','Doctor_Qualifications', 'Doctor_Specialization', 'Doctor_Experience')

        labels = {'Doctor_First_Name': "First Name",
                  'Doctor_Last_Name': "Last Name",
                  'Doctor_Gender': "Gender",
                  'Doctor_DOB': 'Date of Birth',
                  'Doctor_Phone_Number': 'Phone Number',
                  'Doctor_Picture': 'Picture',
                  'Doctor_Qualifications': 'Qualifications',
                  'Doctor_Specialization': 'Specialization',
                  'Doctor_Experience': 'Years of Experience',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data['Doctor_Picture']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
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


weekDay = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class doctorScheduleForm(forms.ModelForm):

    m_interval = forms.IntegerField(widget=forms.Select(choices=slotTimeChoices), initial='10')
    m_openTime = forms.TimeField(widget=forms.Select(choices=m_HOUR_CHOICES), label="opening time", required=False)
    m_closeTime = forms.TimeField(widget=forms.Select(choices=m_HOUR_CHOICES), label="closing time", required=False)

    e_interval = forms.IntegerField(widget=forms.Select(choices=slotTimeChoices), initial='10')
    e_openTime = forms.TimeField(widget=forms.Select(choices=e_HOUR_CHOICES), label="opening time", required=False)
    e_closeTime = forms.TimeField(widget=forms.Select(choices=e_HOUR_CHOICES), label="closing time", required=False )

    def __init__(self, *args, **kwargs):
        super(doctorScheduleForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['day'].widget.attrs['readonly'] = True

    class Meta:
        model = doctorSchedule
        fields = ('day',)
        readonly_fields = ('day',)


scheduleFormset = formset_factory(doctorScheduleForm, extra=0)


class editDoctorScheduleForm(forms.ModelForm):
    m_interval = forms.IntegerField(widget=forms.Select(choices=slotTimeChoices), initial='10')
    m_openTime = forms.TimeField(widget=forms.Select(choices=m_HOUR_CHOICES), label="opening time", required=False)
    m_closeTime = forms.TimeField(widget=forms.Select(choices=m_HOUR_CHOICES), label="closing time", required=False)

    e_interval = forms.IntegerField(widget=forms.Select(choices=slotTimeChoices), initial='10')
    e_openTime = forms.TimeField(widget=forms.Select(choices=e_HOUR_CHOICES), label="opening time", required=False)
    e_closeTime = forms.TimeField(widget=forms.Select(choices=e_HOUR_CHOICES), label="closing time", required=False )

    def __init__(self, *args, **kwargs):
        super(editDoctorScheduleForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['day'].widget.attrs['readonly'] = True

    class Meta:
        model = doctorSchedule
        fields = ('day',)
        readonly_fields = ('day',)


editScheduleFormset = formset_factory(editDoctorScheduleForm, extra=0)


