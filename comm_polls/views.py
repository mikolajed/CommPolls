from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserUpdateForm


def home(request):
    return render(request, "comm_polls/home.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("comm_polls:home")
    else:
        form = SignUpForm()
    return render(request, "comm_polls/signup.html", {"form": form})


def account_settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account details have been updated.')
            return redirect('comm_polls:account_settings')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'comm_polls/account_settings.html', {'form': form})
