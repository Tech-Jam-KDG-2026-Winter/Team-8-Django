from django.db import models
from django.contrib.auth.models import User

class MenuPost(models.Model):
    #投稿者#
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #料理名#
    title = models.CharField(max_length=100)
    #材料#
    ingredients = models.TextField()
    #作り方(手順) 例：1. 玉ねぎを切る 2. 卵を焼く 3. ご飯と混ぜる#
    recipe = models.TextField(blank=True)
    #料理の写真#
    image = models.ImageField(upload_to='menus/', blank=True)
    #投稿日#
    created_at = models.DateTimeField(auto_now_add=True)    
    #栄養素#
    calories = models.IntegerField('カロリー(kcal)', default=0)
    protein = models.FloatField('たんぱく質(g)', default=0)
    fat = models.FloatField('脂質(g)', default=0)
    carbs = models.FloatField('炭水化物(g)', default=0)

    def __str__(self):
        return self.title