from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import Profile

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("accounts:profile")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:profile")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect("accounts:login")
    return render(request, "accounts/logout_confirm.html")


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.username},
    )
    if not profile.name:
        profile.name = request.user.username
        profile.save(update_fields=["name"])

    context = {
        "registration_user_name": profile.name,
        "user_age": profile.age,
        "user_height": profile.height_cm,
        "user_weight": profile.weight_kg,
        "user_gender": profile.get_gender_display() if profile.gender else "未回答",
    }
    return render(request, "accounts/profile.html", context)
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import Profile

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts:profile")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("accounts:profile")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("accounts:login")
    return render(request, "accounts/logout_confirm.html")


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.username},
    )
    context = {
        "registration_user_name": profile.name,
        "user_age": profile.age,
        "user_height": profile.height_cm,
        "user_weight": profile.weight_kg,
        "user_gender": profile.get_gender_display(),
    }
    return render(request, "accounts/profile.html", context)
