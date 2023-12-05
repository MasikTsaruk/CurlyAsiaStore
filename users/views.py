from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from .tasks import send_notification_mail


def login_user(response):
    if response.method == 'POST':
        form = LoginForm(response.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(response, username=username, password=password)
            message = "You're logged in as  " + username
            mail = user.email
            send_notification_mail.delay(mail, message)
            if user:
                login(response, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(response, 'Vers/Login.html', {
        'form': form
    })


def signup(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            message = "You're registrated on out site! "
            mail = form.cleaned_data['email']
            send_notification_mail.delay(mail, message)
            return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "Vers/Register.html", {
        "form": form
    })


def logout_user(response):
    logout(response)
    return redirect('/')
