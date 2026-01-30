from django.db import models

class Recipe(models.Model):
    #料理・献立データを管理するモデル

    title = models.CharField('料理名', max_length=100)
    description = models.TextField('説明', blank=True)
    
    # 栄養素
    calories = models.IntegerField('カロリー(kcal)')
    protein = models.FloatField('タンパク質(g)', default=0)
    fat = models.FloatField('脂質(g)', default=0)
    carbs = models.FloatField('炭水化物(g)', default=0)

    # カテゴリ（間食を削除し、3食のみに限定）
    CATEGORY_CHOICES = (
        ('morning', '朝食'),
        ('lunch', '昼食'),
        ('dinner', '夕食'),
    )
    category = models.CharField('カテゴリ', max_length=20, choices=CATEGORY_CHOICES, default='dinner')

    # 画像
    image = models.ImageField('料理写真', upload_to='recipes/', blank=True, null=True)

    def __str__(self):
        return self.title