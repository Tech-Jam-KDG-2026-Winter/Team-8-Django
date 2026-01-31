from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Profile

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