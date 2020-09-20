from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, UserEditForm, ProfileEditForm
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib.auth.models import User

# Create your views here
from .models import Profile


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        user_name = login_form.cleaned_data.get('user_name')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            login_form.add_error('user_name', 'کاربری با مشخصات وارد شده یافت نشد')

    context = {
        'login_form': login_form,
        'title': 'ورود'
    }
    return render(request, 'account/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    register_form = RegisterForm(request.POST or None)

    if register_form.is_valid():
        user_name = register_form.cleaned_data.get('user_name')
        password = register_form.cleaned_data.get('password')
        email = register_form.cleaned_data.get('email')
        user = User.objects.create_user(username=user_name, email=email, password=password)
        Profile.objects.create(user=user)
        return redirect('/login')

    context = {
        'register_form': register_form,
        'title': 'ثبت نام'
    }
    return render(request, 'account/register.html', context)


def log_out(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form, 'title': 'حساب کاربری'})
