# Django Team Starter

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install django==5.1.2
python manage.py migrate
python manage.py runserver
```

## Endpoints
- /           root check
- /healthz/   health check
- /admin/     django admin