# Habito（Tec-Jam Team8）

食事・健康習慣の記録からレシピ提案ができる Django アプリ

- **ダッシュボード**：今日の生活ログを入力 → スコア算出＆改善アドバイス表示
- **レシピ提案**：健康に合わせて、レシピをランダムに提案
- **投稿（みんなの投稿）**：ユーザーが献立/料理を投稿して一覧・詳細表示
- **マイページ**：ユーザープロフィール（名前/年齢/身長/体重/性別）管理


## ディレクトリ構成

```
tec-jam/
├─ apps/
│  ├─ core/        # ダッシュボード・レシピ表示
│  ├─ contents/    # 投稿（みんなの投稿）
│  └─ accounts/    # ログイン/サインアップ/マイページ
├─ config/         # Django 設定（settings/urls/wsgi/asgi）
├─ templates/      # 共通テンプレート
├─ static/         # CSS/JS/画像
├─ media/          # アップロード画像（開発時）
├─ data.csv        # レシピ初期データ（CSV）
├─ make_csv.py     # data.csv 生成スクリプト
└─ manage.py
```

---

## 必要要件

- Python **3.10+**
- pip


---

## セットアップ（ローカル起動）


git clone https://github.com/Tech-Jam-KDG-2026-Winter/Team-8-Django.git
cd tec-jam

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate


### 初期データ投入（任意だけど推奨）

#### レシピデータ（CSV → DB）

python manage.py import_recipes

python make_csv.py

#### 投稿サンプル（みんなの投稿）

python manage.py seed_posts

- `seed_user / password1234` のユーザーが作られ、サンプル投稿が入ります。

###  管理ユーザー作成（任意）

python manage.py createsuperuser
 サーバー起動

python manage.py runserver

ブラウザで以下へアクセス：

- トップ（ダッシュボードへリダイレクト）：`http://127.0.0.1:8000/`
- ダッシュボード：`http://127.0.0.1:8000/core/dashboard/`
- レシピ提案：`http://127.0.0.1:8000/core/recommend/`
- 投稿一覧：`http://127.0.0.1:8000/contents/`
- ログイン：`http://127.0.0.1:8000/accounts/login/`
- 管理画面：`http://127.0.0.1:8000/admin/`

---

## 主な機能

###  ダッシュボード（健康スコア）

- 今日の行動（運動・食事記録・生活習慣）を入力
- スコアを計算し、改善優先度の高いアドバイスを最大3件表示

関連：`apps/core/models.py`（`DailyHealthLog.calculate_score`）

###  レシピ提案

- 時間帯（朝/昼/夜）に応じてカテゴリを切り替え
- 目標カロリー（基礎代謝 × 活動量から算出）を 3分割して1食の目安を出し、
  その付近のレシピを優先して提案

関連：`apps/core/views.py`（`recommend_view`）

###  投稿（みんなの投稿）

- 投稿一覧：`/contents/`
- 投稿作成：`/contents/create/`（ログイン必須）
- 投稿詳細：`/contents/<id>/`

関連：`apps/contents/models.py`, `apps/contents/views.py`

###  認証・マイページ

- サインアップ：`/accounts/signup/`
- ログイン：`/accounts/login/`
- マイページ：`/accounts/profile/`
- マイページ編集：`/accounts/profile/mypage-edit.html`

関連：`apps/accounts/*`

---

## 画像アップロードについて

- 投稿画像：`apps/contents.models.MenuPost.image`（`upload_to='menus/'`）
- レシピ画像：`apps/core.models.Recipe.image`（`upload_to='recipes/'`）

開発環境では `MEDIA_URL=/media/` と `MEDIA_ROOT=BASE_DIR/media` を使用しています。

---

## 開発ルール

- 自分名前をブランチ名にする

---

## 作成者

---中川　バックエンド(account)　リーダー　
---林　　バックエンド(core)
---大木　バックエンド(contents)
---箸尾　フロントエンド
---藤原　デザイン
