from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MenuPost # モデル名を MenuPost に合わせる

@login_required
def create_view(request):
    # apps/contents/views.py の create_view 関数内
    if request.method == 'POST':
    # .create() の戻り値を post という変数で受け取る
        post = MenuPost.objects.create(
            user=request.user,
            title=request.POST.get('name'),
            ingredients=request.POST.get('ingredients'),
            recipe=request.POST.get('recipe'),
            calories=request.POST.get('calories') or 0,
            protein=request.POST.get('protein') or 0,
            fat=request.POST.get('fat') or 0,
            carbs=request.POST.get('carbs') or 0,
            image=request.FILES.get('image'),
    )
    # 保存した投稿のID(pk)を使って、詳細画面(detail)へリダイレクト！
    return redirect('contents:detail', pk=post.pk)

    # 投稿画面を表示
    return render(request, 'contents/post.html') # あなたが作っているHTMLのパス

# apps/contents/views.py に追記
def index_view(request):
    # すべての投稿を、新しい順（-created_at）に取得
    posts = MenuPost.objects.all().order_by('-created_at')
    # index.html に 'posts' という名前でデータを渡す
    return render(request, 'contents/index.html', {'posts': posts})