from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Recipe
import datetime # 時間判定のために必要

@login_required
def recommend_view(request):
    user = request.user
    
    # ---------------------------------------------------------
    # 1. 基礎代謝と必要カロリーの計算（性別・体重・身長考慮）
    # ---------------------------------------------------------
    # デフォルト値（データがない人用）
    target_calories = 2000 
    
    # ユーザーがプロフィールを持っているか確認
    if hasattr(user, 'profile'):
        p = user.profile
        # 必要なデータが揃っているか確認
        if p.weight and p.height and p.age and p.gender:
            # --- ハリス・ベネディクトの式 ---
            if p.gender == 'male':
                # 男性: 66.5 + (13.75 × 体重) + (5.003 × 身長) - (6.75 × 年齢)
                bmr = 66.5 + (13.75 * p.weight) + (5.003 * p.height) - (6.75 * p.age)
            elif p.gender == 'female':
                # 女性: 655.1 + (9.563 × 体重) + (1.850 × 身長) - (4.676 × 年齢)
                bmr = 655.1 + (9.563 * p.weight) + (1.850 * p.height) - (4.676 * p.age)
            else:
                # その他・未設定の場合は男性式をベースに少し調整などのロジックを入れる（今回は男性式で代用）
                bmr = 66.5 + (13.75 * p.weight) + (5.003 * p.height) - (6.75 * p.age)

            # 活動レベルを掛けてTDEE（総消費カロリー）を算出
            target_calories = int(bmr * p.activity_level)

    # 1食あたりの目安（3食均等割り）
    meal_calories = int(target_calories / 3)

    # ---------------------------------------------------------
    # 2. 時間帯によるカテゴリ判定（朝からステーキ問題の解決）
    # ---------------------------------------------------------
    current_hour = datetime.datetime.now().hour
    
    # 時間帯のロジック
    if 4 <= current_hour < 11:
        # 朝食: 04:00 - 11:00
        current_category = 'morning'
        time_label = "朝食"
    elif 11 <= current_hour < 17:
        # 昼食: 11:00 - 17:00
        current_category = 'lunch'
        time_label = "ランチ"
    else:
        # 夕食: 17:00 - 04:00
        current_category = 'dinner'
        time_label = "夕食"

    # ---------------------------------------------------------
    # 3. データベースからの剪定（フィルタリング）
    # ---------------------------------------------------------
    # カロリーの許容範囲（目安の前後 200kcal）
    min_cal = meal_calories - 200
    max_cal = meal_calories + 200
    
    # 【重要】カテゴリ と カロリー の両方で絞り込む
    recommended_recipes = Recipe.objects.filter(
        category=current_category,      # ★今の時間帯に合ったものだけ！
        calories__gte=min_cal,          # カロリー下限
        calories__lte=max_cal           # カロリー上限
    ).order_by('?')[:3] # ランダムに3つ

    # もし条件が厳しすぎて0件だった場合の救済措置
    # （カテゴリだけは守りつつ、カロリー制限を外して検索）
    if not recommended_recipes:
        recommended_recipes = Recipe.objects.filter(
            category=current_category
        ).order_by('?')[:3]

    # それでもなければ全件から（最終手段）
    if not recommended_recipes:
         recommended_recipes = Recipe.objects.all().order_by('?')[:3]

    context = {
        'target_calories': target_calories,
        'meal_calories': meal_calories,
        'time_label': time_label,       # 画面表示用「今は〇〇の時間です」
        'recipes': recommended_recipes,
    }
    
    return render(request, 'core/recommend.html', context)