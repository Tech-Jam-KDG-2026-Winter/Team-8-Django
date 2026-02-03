from django.urls import path
from . import views
app_name = 'core'

urlpatterns = [
    path('recommend/', views.recommend_view, name='recommend'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]