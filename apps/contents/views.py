from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MenuPost

# 投稿一覧画面
def index_view(request):
    posts = MenuPost.objects.all() 
    return render(request, 'contents/post.html', {'posts': posts})

# 投稿詳細画面 (ここが urls.py から呼ばれる detail_view です)
def detail_view(request, pk):
    post = get_object_or_404(MenuPost, pk=pk)
    return render(request, 'contents/post-detail.html', {'post': post})

# 新規投稿画面
@login_required
def create_view(request):
    if request.method == 'POST':
        # フォームから送られてきたデータを保存
        post = MenuPost.objects.create(
            user=request.user,
            title=request.POST.get('name'),    
            ingredients=request.POST.get('ingredients'),
            ingredients_num=request.POST.get('ingredients_num'),
            recipe=request.POST.get('recipe'), 
            image=request.FILES.get('image'),  
        )
        # 保存したら詳細画面へリダイレクト
        return redirect('contents:detail', pk=post.pk)

    # 投稿用ページを表示（ファイル名はプロジェクトに合わせて post.html などに修正してください）
    return render(request, 'contents/post.html')