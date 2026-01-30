from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "age", "gender", "height_cm", "weight_kg", "updated_at")
    search_fields = ("user__username", "name")
