from django import forms
from .models import MenuPost

class MenuPostForm(forms.ModelForm):
    class Meta:
        model = MenuPost
        # ユーザーに入力させたい項目を指定
        fields = ['title', 'ingredients', 'recipe', 'image', 'calories', 'protein', 'fat', 'carbs']