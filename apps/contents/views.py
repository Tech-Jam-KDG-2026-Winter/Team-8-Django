from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe

@login_required
def create_view(request):
    if request.method == 'POST':
        Recipe.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            ingredients=request.POST.get('ingredients'),
            recipe=request.POST.get('recipe'),
            calories=request.POST.get('calories'),
            protein=request.POST.get('protein'),
            fat=request.POST.get('fat'),
            carbs=request.POST.get('carbs'),
            image=request.FILES.get('image'),
            category=request.POST.get('category'),
        )
        return redirect('core:recipe_list')

    return render(request, 'core/recipe_create.html')
