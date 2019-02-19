from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import  password_validation

from .models import *

class RegistroForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4,
                                                                max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password',
                                                    widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                                    widget=forms.PasswordInput)

    class Meta:
        model = User

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = userProfile
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'})
            }
