from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class Recipe(models.Model):
    # 料理・献立データ
    title = models.CharField('料理名', max_length=100)
    description = models.TextField('説明', blank=True)
    calories = models.IntegerField('カロリー(kcal)')
    protein = models.FloatField('タンパク質(g)', default=0)
    fat = models.FloatField('脂質(g)', default=0)
    carbs = models.FloatField('炭水化物(g)', default=0)
    CATEGORY_CHOICES = (
        ('morning', '朝食'),
        ('lunch', '昼食'),
        ('dinner', '夕食'),
    )
    category = models.CharField('カテゴリ', max_length=20, choices=CATEGORY_CHOICES, default='dinner')
    image = models.ImageField('料理写真', upload_to='recipes/', blank=True, null=True)

    def __str__(self):
        return self.title


class HealthProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    
    # 目標スコア（ユーザーが決める）
    target_score = models.IntegerField('目標スコア', default=80)

    # 運動のベースラインを5段階に拡張
    ACTIVITY_CHOICES = (
        (20, 'Lv1: ほぼ座りっぱなし (20点)'),
        (40, 'Lv2: 通勤・通学程度 (40点)'),
        (60, 'Lv3: 軽い運動習慣あり (60点)'),
        (80, 'Lv4: 運動習慣あり (80点)'),
        (100, 'Lv5: ジム等で体を動かす (100点)'),
    )
    base_activity_score = models.IntegerField('普段の運動', choices=ACTIVITY_CHOICES, default=40)
    
    # 生活習慣（基本減点）
    is_smoker = models.BooleanField('喫煙習慣 (-20点)', default=False)
    drinks_daily = models.BooleanField('毎日の飲酒 (-20点)', default=False)
    low_water = models.BooleanField('水分不足 (-10点)', default=False)
    high_stress = models.BooleanField('ストレスが高い (-10点)', default=False)

    def __str__(self):
        return f"{self.user.username}の健康プロフィール"


class DailyHealthLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('記録日', default=datetime.date.today)

    # --- A. 運動変動 ---
    MOVEMENT_CHOICES = (
        (10, 'いつもより動いた (+10)'),
        (0, 'いつも通り (0)'),
        (-10, '動かなかった (-10)'),
    )
    movement_diff = models.IntegerField('今日の運動量', choices=MOVEMENT_CHOICES, default=0)

    # --- B. 食事記録 ---
    meals_count = models.IntegerField('食事記録回数', default=0, help_text='0~3回')
    
    # 栄養フラグ
    protein_ok = models.BooleanField('タンパク質80%以上', default=False)
    fat_ok = models.BooleanField('脂質適正', default=False)
    veggies_ok = models.BooleanField('野菜適正', default=False)
    
    # バランスフラグ
    late_night_meal = models.BooleanField('22時以降の食事 (-10)', default=False)
    skip_breakfast = models.BooleanField('朝食抜き (-10)', default=False)
    good_balance = models.BooleanField('3食バランス良好 (+20)', default=False)

    # --- C. 生活習慣変動 ---
    sleep_quality_good = models.BooleanField('睡眠の質が良い', default=False)
    mental_good = models.BooleanField('メンタル良好', default=False)

    class Meta:
        unique_together = ('user', 'date')
        # 【重要】履歴グラフ化のために日付順で並ぶようにする
        ordering = ['-date'] 

    # =========================================================
    #  🔥 スコア計算 & アドバイス抽出ロジック Ver.2
    # =========================================================
    def calculate_score(self):
        # 改善候補リスト： (重み, メッセージ) のタプルを入れる
        # 重みが大きいほど「改善した時の効果」が高い＝優先度が高い
        improvement_candidates = []

        # 1. 基礎代謝 (20%) - 固定
        bmr_part = 100 * 0.2

        # 2. 運動 (30%)
        base_act = 40 # デフォルト
        if hasattr(self.user, 'health_profile'):
            base_act = self.user.health_profile.base_activity_score
        
        # 運動のアドバイス判定
        act_raw = base_act + self.movement_diff
        if self.movement_diff < 0:
            improvement_candidates.append((10, "今日は運動不足でした。一駅歩くなど工夫しましょう。"))
        
        act_part = min(100, max(0, act_raw)) * 0.3

        # 3. 食事 (30%)
        # a. 記録率
        rec_score = 0
        if self.meals_count >= 3: rec_score = 40
        elif self.meals_count == 2: rec_score = 25
        else: rec_score = 10
        
        if self.meals_count < 3:
            # 記録をつけるだけで点数が跳ね上がるので重み大(30点相当)
            improvement_candidates.append((30, "食事記録を全てつけるだけでスコアが大幅アップします！"))

        # b. 栄養
        nut_score = 0
        if self.protein_ok: nut_score += 20
        else: improvement_candidates.append((20, "筋肉の源、タンパク質が不足しています！肉・魚・豆を食べましょう。"))
        
        if self.fat_ok: nut_score += 10
        if self.veggies_ok: nut_score += 10
        else: improvement_candidates.append((10, "野菜不足です。ビタミン摂取で代謝を上げましょう。"))

        # c. バランス
        bal_score = 0
        if self.late_night_meal: 
            bal_score -= 10
            improvement_candidates.append((15, "22時以降の食事は脂肪になりやすいです。控えましょう。"))
        if self.skip_breakfast: 
            bal_score -= 10
            improvement_candidates.append((15, "朝食抜きは代謝を下げます。バナナだけでも食べましょう。"))
        if self.good_balance: bal_score += 20
        
        diet_raw = rec_score + nut_score + bal_score
        diet_part = min(100, max(0, diet_raw)) * 0.3

        # 4. 生活習慣 (20%)
        life_raw = 60 # 初期値
        if hasattr(self.user, 'health_profile'):
            hp = self.user.health_profile
            if hp.is_smoker: 
                life_raw -= 20
                improvement_candidates.append((20, "禁煙は最大の健康投資です。スコアが大きく改善します。"))
            if hp.drinks_daily: 
                life_raw -= 20
                improvement_candidates.append((20, "休肝日を作りましょう。睡眠の質も向上します。"))
            if hp.low_water: 
                life_raw -= 10
                improvement_candidates.append((10, "水分不足は代謝ダウンの元。こまめに水を飲みましょう。"))
            if hp.high_stress: life_raw -= 10
        
        if self.sleep_quality_good: life_raw += 10
        else: improvement_candidates.append((10, "睡眠の質を上げると回復力が高まります。寝る前のスマホを控えましょう。"))
        
        if self.mental_good: life_raw += 10

        life_part = min(100, max(0, life_raw)) * 0.2

        # --- 合計スコア ---
        total_score = int(bmr_part + act_part + diet_part + life_part)

        # --- アドバイスの選定（トップ3） ---
        # 重み(weight)が大きい順（降順）にソート
        improvement_candidates.sort(key=lambda x: x[0], reverse=True)
        
        # 上位3つのメッセージだけを取り出す
        final_advice_list = [item[1] for item in improvement_candidates[:3]]

        # もしアドバイスがなければ褒める
        if not final_advice_list:
            final_advice_list.append("完璧です！この調子でキープしましょう！")

        return total_score, final_advice_list