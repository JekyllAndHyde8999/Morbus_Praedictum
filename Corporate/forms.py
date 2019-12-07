from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from tempus_dominus.widgets import TimePicker
import datetime as dt
from django.forms import formset_factory

from .models import Company, HospitalAddress, Area, City

# Form for Signing Up.
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Input a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class UserProfileInfoForm(forms.ModelForm):
    Comapny_Logo = forms.ImageField(label=('Logo Photo'), required=False, error_messages = {'invalid':("Image files only.")}, 
    widget=forms.FileInput)
    
    class Meta:
        model = Company
        fields = ('Company_Name', 'Company_Logo', 'Company_Phone_Number', 'Company_License_Number')
        labels = {'Company_Name':"Name of the Organisation",
        'Company_License_Number':'License Number',
        'Company_Email':'Email ID',
        'Company_Phone_Number':'Phone Number',
        'Company_Logo':'Logo Photo'}

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
    Company_Logo = forms.ImageField(label=('Logo Photo'), required=False, error_messages = {'invalid':("Image files only.")}, 
    widget=forms.FileInput)

    class Meta:
        model = Company
        fields = ('Company_Name', 'Company_Logo', 'Company_Phone_Number', 'Company_License_Number')
        labels = {'Company_Name':"Name of the Organisation",
        'Company_License_Number':'License Number',
        'Company_Email':'Email ID',
        'Company_Phone_Number':'Phone Number',
        'Company_Logo':'Logo Photo'}

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
