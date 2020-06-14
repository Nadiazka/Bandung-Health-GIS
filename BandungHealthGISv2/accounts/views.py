from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

# Create your views here.
@transaction.atomic
def registerPage(request):
	form = CreateUserForm()
	profile_form = ProfileForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if form.is_valid() and profile_form.is_valid():
			form.save()
			profile_form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Selamat '+ user +', akun kamu berhasil dibuat')
			return redirect('login')

	context = {
	'form' : form, 
	'profile_form' : profile_form
	}
	return render (request, 'accounts/register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			messages.info(request, 'Username atau Password salah')

	return render (request, 'accounts/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

@transaction.atomic
def editProfile(request):
	form = UserChangeForm()
	profile_form = ProfileForm()

	if request.method == 'POST':
		form = UserChangeForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if form.is_valid() and profile_form.is_valid():
			form.save()
			profile_form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Selamat '+ user +', akun kamu berhasil diubah')
			return redirect('index')

	context = {
	'form' : form, 
	'profile_form' : profile_form
	}
	return render (request, 'accounts/editProfile.html', context)	

def changePasswordPage(request):
	form = PasswordChangeForm(user=request.user)

	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Selamat '+ user +', password kamu berhasil diubah')
			return redirect('editProfile')

	context = {'form' : form}
	return render (request, 'accounts/changePass.html', context)

def edit_user(request, pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=pk)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)

    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('website', 'bio', 'phone', 'city', 'country', 'organization'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/accounts/profile/')

        return render(request, "account/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied