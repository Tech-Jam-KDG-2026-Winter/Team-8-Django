from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import SignUpForm
from .models import Profile


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            next_url = request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            return redirect("accounts:profile")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())

            next_url = request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

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
        defaults={
            "name": request.user.username,
            "gender": "other", 
        },
    )

    context = {
        "registration_user_name": profile.name,
        "user_age": profile.age,
        "user_height": profile.height_cm,
        "user_weight": profile.weight_kg,
        "user_gender": profile.get_gender_display() if profile.gender else "未回答",
    }
    return render(request, "accounts/mypage.html", context)


@login_required
def mypage_edit_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "gender": "other",  
        },
    )

    if request.method == "POST":
        profile.name = request.POST.get("name", "").strip()
        profile.age = request.POST.get("age") or None
        profile.height_cm = request.POST.get("height_cm") or None
        profile.weight_kg = request.POST.get("weight_kg") or None
        gender = request.POST.get("gender")
        if gender:
            profile.gender = gender
        else:
            profile.gender = profile.gender or "other"

        profile.save()
        return redirect("accounts:profile")

    return render(request, "accounts/mypage-edit.html", {"profile": profile})
