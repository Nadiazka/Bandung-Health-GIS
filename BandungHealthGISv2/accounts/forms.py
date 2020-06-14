from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import *
			
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['id_dinkes']

"""
			
class EditProfileForm(UserChangeForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['id_dinkes']

    def save(self, user=None):
        user_profile = super(EditProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile
"""