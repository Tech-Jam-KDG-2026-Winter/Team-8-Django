from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
#from .models import MenuPost

class MenuPost(models.Model):
    #投稿者#
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #料理名#
    title = models.CharField(max_length=100)
    #材料#
    ingredients = models.TextField()
    #材料の量#
    ingredients_num = models.TextField() 
    #作り方(手順) 例：1. 玉ねぎを切る 2. 卵を焼く 3. ご飯と混ぜる#
    recipe = models.TextField(blank=True)
    #料理の写真#
    image = models.ImageField(upload_to='menus/', blank=True)   

    def __str__(self):
        return self.title

#指定されたIDの投稿データを取得して、HTML（テンプレート）に渡す処理    
def detail_view(request, pk):
    # pk（ID）を使って、特定の投稿データを1件取得
    post = get_object_or_404(MenuPost, pk=pk)
    # 'post' という名前でHTML側にデータを渡す
    return render(request, 'contents/detail.html', {'post': post})