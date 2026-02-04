from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .models import HealthProfile, DailyHealthLog
import datetime 
from apps.contents.models import MenuPost 

@login_required
def recommend_view(request):
    user = request.user
    
    # --- 1. 基礎代謝と必要カロリー ---
    target_calories = 2000 
    
    if hasattr(user, 'health_profile'):  
        p = user.health_profile
        if p.weight and p.height and p.age and p.gender:
            if p.gender == 'male':
                bmr = 66.5 + (13.75 * p.weight) + (5.003 * p.height) - (6.75 * p.age)
            elif p.gender == 'female':
                bmr = 655.1 + (9.563 * p.weight) + (1.850 * p.height) - (4.676 * p.age)
            else:
                bmr = 66.5 + (13.75 * p.weight) + (5.003 * p.height) - (6.75 * p.age)

            target_calories = int(bmr * p.activity_level)

    meal_calories = int(target_calories / 3)

    # --- 2. 時間帯判定 ---
    current_hour = datetime.datetime.now().hour
    
    if 4 <= current_hour < 11:
        current_category = 'morning'
        time_label = "朝食"
    elif 11 <= current_hour < 17:
        current_category = 'lunch'
        time_label = "ランチ"
    else:
        current_category = 'dinner'
        time_label = "夕食"

    # --- 3. データベース検索 ---
    min_cal = meal_calories - 200
    max_cal = meal_calories + 200
    
    recommended_recipes = Recipe.objects.filter(
        category=current_category,
        calories__gte=min_cal,
        calories__lte=max_cal
    ).order_by('?')[:3]

    if not recommended_recipes:
        recommended_recipes = Recipe.objects.filter(
            category=current_category
        ).order_by('?')[:3]

    if not recommended_recipes:
         recommended_recipes = Recipe.objects.all().order_by('?')[:3]

    context = {
        'target_calories': target_calories,
        'meal_calories': meal_calories,
        'time_label': time_label,
        'recipes': recommended_recipes,
    }
    
    return render(request, 'core/recommend.html', context)


@login_required
def dashboard_view(request):
    user = request.user
    today = datetime.date.today()

    # 1. 今日のログを取得（なければ作る）
    daily_log, created = DailyHealthLog.objects.get_or_create(
        user=user,
        date=today
    )
    
    # 2. 基本プロフィールがなければ仮作成
    if not hasattr(user, 'health_profile'):
        HealthProfile.objects.create(user=user)

    # 3. フォームからPOSTが来た場合の処理
    if request.method == 'POST':
        # A. 運動
        if 'movement_diff' in request.POST:
            daily_log.movement_diff = int(request.POST['movement_diff'])
        
        # B. 食事回数
        if 'meals_count' in request.POST:
            daily_log.meals_count = int(request.POST['meals_count'])

        # C. チェックボックス系
        daily_log.protein_ok = 'protein_ok' in request.POST
        daily_log.veggies_ok = 'veggies_ok' in request.POST
        daily_log.late_night_meal = 'late_night_meal' in request.POST
        daily_log.skip_breakfast = 'skip_breakfast' in request.POST
        daily_log.sleep_quality_good = 'sleep_quality_good' in request.POST
        
        # 保存する
        daily_log.save()
        
        # PRGパターンでリダイレクト
        return redirect('core:dashboard')

    # 4. スコア計算
    score, advice_list = daily_log.calculate_score()

    # 5. 献立提案（公式レシピ）の取得
    current_hour = datetime.datetime.now().hour
    if 4 <= current_hour < 11:
        current_category = 'morning'
    elif 11 <= current_hour < 17:
        current_category = 'lunch'
    else:
        current_category = 'dinner'

    recipes = Recipe.objects.filter(category=current_category).order_by('?')[:3]

    if not recipes:
        recipes = Recipe.objects.all().order_by('?')[:3]

    # 6. 目標スコア計算
    target_score = 80
    if hasattr(user, 'health_profile'):
        target_score = user.health_profile.target_score

    points_to_target = max(0, target_score - score)

    # 新しい順（idの降順）で取得する
    posts = MenuPost.objects.order_by('-id')

    context = {
        'score': score,
        'target_score': target_score,
        'points_to_target': points_to_target,
        'advice_list': advice_list,
        'daily_log': daily_log, 
        'recipes': recipes, # 公式レシピ（献立提案用）
        'posts': posts,     # ★追加：みんなの投稿（HTMLで for post in posts と使う）
    }

    return render(request, 'core/home.html', context)


@login_required
def detail_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    materials = [line.strip() for line in (recipe.ingredients or "").splitlines() if line.strip()]
    steps = [line.strip() for line in (recipe.steps or "").splitlines() if line.strip()]

    return render(request, "core/detail.html", {
        "recipe": recipe,
        "materials": materials,
        "steps": steps,
    })