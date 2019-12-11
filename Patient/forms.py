from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from .models import Address, Area, City, Profile
from django.core.validators import MinValueValidator, MaxValueValidator
import os
import pickle

from Patient.models import City
from django.forms import formset_factory


cityChoiceList = City.objects.values_list('name', flat=True).distinct()
#
temp = [(i, i) for i in cityChoiceList]
# temp = []
temp.append((None, 'Choose City'))

cityChoice = tuple(temp)

SYMPTOMS_FILE_PATH = os.path.join("Pickles", "symptom_labels.pkl")
with open(SYMPTOMS_FILE_PATH, mode="rb") as f:
    symptoms_list = pickle.load(f).tolist()

temp2 = [(str(i), str(i)) for i in symptoms_list]
temp2.append((None, '--blank--'))

symptomChoice = tuple(temp2)

specializationChoices = (
    (None, 'Choose Specialization'),
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10')
)


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
        model = Profile
        widgets = {
            'Patient_DOB': DateInput()
        }
        fields = ('Patient_First_Name', 'Patient_Last_Name', 'Patient_Gender', 'Patient_Picture', 'Patient_DOB',
                  'Patient_Blood_Group', 'Patient_Blood_Donation', 'Patient_Phone_Number')
        labels = {'Patient_First_Name': "First Name",
                  'Patient_Last_Name': "Last Name",
                  'Patient_Gender': "Gender",
                  'Patient_DOB': 'Date of Birth',
                  'Patient_Blood_Group': 'Blood Group',
                  'Patient_Blood_Donation': 'Would you like to donate blood when required?',
                  'Patient_Phone_Number': 'Phone Number',
                  'Patient_Picture': 'Picture'}

    def clean_avatar(self):
        avatar = self.cleaned_data['Patient_Picture']

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
        model = Address
        fields = ('Home', 'Street', 'city', 'area', 'Pin')

    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()
        print(self.fields['area'].queryset)

        print(self.instance.pk)

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['area'].queryset = Area.objects.filter(
                    city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty city queryset
        elif self.instance.pk:
            self.fields['area'].queryset = self.instance.city.area_set.order_by(
                'name')


class CustomUserEditForm(forms.ModelForm):
    Patient_Picture = forms.ImageField(label='Picture', required=False, error_messages={'invalid': "Image files only."},
                                       widget=forms.FileInput)
    
    class Meta:
        widgets = {
            'Patient_DOB': DateInput()
        }
        model = Profile
        fields = ('Patient_First_Name', 'Patient_Last_Name', 'Patient_Gender', 'Patient_Picture', 'Patient_DOB',
                  'Patient_Blood_Group', 'Patient_Blood_Donation', 'Patient_Phone_Number')
        labels = {'Patient_First_Name': "First Name",
                  'Patient_Last_Name': "Last Name",
                  'Patient_Gender': "Gender",
                  'Patient_DOB': 'Date of Birth',
                  'Patient_Blood_Group': 'Blood Group',
                  'Patient_Blood_Donation': 'Would you like to donate blood when required?',
                  'Patient_Phone_Number': 'Phone Number',
                  'Patient_Picture': 'Picture'}

    def clean_avatar(self):
        avatar = self.cleaned_data['Patient_Picture']

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


class doctorSearchForm(forms.Form):
    docName = forms.CharField(max_length=50,required=False)
    docCity = forms.CharField(widget=forms.Select(choices=cityChoice), required=False, initial='--blank--')
    docSpecial = forms.IntegerField(widget=forms.Select(choices=specializationChoices),
                                    required=False, initial='--blank--')


class PredictForm(forms.Form):
    # xwz = forms.ChoiceField(choices=symptomChoice)
    name = forms.ChoiceField(label='Symptom',
                             # widget=forms.Select(choices=symptomChoice)
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             choices=symptomChoice
                             )

    # def __init__(self, *args, **kwargs):
    #     super(PredictForm, self).__init__(*args, **kwargs)

PredictFormset = formset_factory(PredictForm)
PredictFormset.form.base_fields['name'] = forms.ChoiceField(choices=symptomChoice)

