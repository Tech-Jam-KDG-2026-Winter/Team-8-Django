# Django Team Starter

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install django==6.0.1
python manage.py migrate
python manage.py runserver
```

## Endpoints
- /           root check
- /healthz/   health check
- /admin/     django admin



## 開発ルール
- main / develop 直編集禁止
- feature ブランチ必須
- PR必須

## 起動方法
### Java
cd backend-java
./gradlew bootRun

### Django
cd backend-django
python manage.py runserver


--test