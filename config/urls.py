# config/urls.py
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='core:dashboard', permanent=False)),
    path('admin/', admin.site.urls),
    path('core/', include('apps.core.urls')), 
    path('contents/', include('apps.contents.urls')),
    path('accounts/', include('apps.accounts.urls')),
]

#画像表示用設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)