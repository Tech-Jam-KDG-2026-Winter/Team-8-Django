from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="ユーザー名", max_length=150)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
