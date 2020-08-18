from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required


def register(request):

    context = {
        'active': 'register',
        'title': 'إنشاء حساب',
        'first_name': '' ,
        'last_name': '' ,
        'email': '' ,
        'mobile': '' ,
    }
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('mobile')
        password = request.POST.get('password')
        hashed_password = make_password(password)

       
        context['first_name'] = first_name
        context['last_name'] = last_name
        context['email'] = email
        context['mobile'] = username

        user1 = User.objects.filter(username=username)
        user2 = User.objects.filter(email=email)

        if user1 and user2:
            messages.warning(request, "رقم الموبايل مرتبط بحساب آخر")
            messages.warning(request, " البريد الالكتروني مرتبط بحساب آخر")
            return render(request, 'users/register.html', context)
        if user1 and not user2:
            messages.warning(request, "رقم الموبايل مرتبط بحساب آخر")
            return render(request, 'users/register.html',context)
        if user2 and not user1:
            messages.warning(request, " البريد الالكتروني مرتبط بحساب آخر")
            return render(request, 'users/register.html',context)
        if not user1 and not user2:
            user = User(username=username, first_name=first_name,
                        last_name=last_name, email=email, password=hashed_password)
            user.save()
            auth_login(request, user)
            messages.success(
                request, f' تم إنشاء حساب باسم {first_name} {last_name}')
            return redirect('cars-home')
   
    return render(request, 'users/register.html', context)


def login(request):
    username = ''
    if request.method == 'POST':
        username = request.POST['mobile']
        password = request.POST['password']
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'تم تسجيل الدخول بنجاح ، مرحبا {user.first_name}')
            return redirect('cars-home')
        else:
            messages.warning(request, 'رقم الموبايل أو كلمة المرور غير صحيحة')

    return render(request, 'users/login.html', {'active': 'login', 'title': 'تسجيل الدخول' , 'mobile':username})


@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'users/logout.html', {'active': 'logout', 'title': 'تسجيل الخروج'})
