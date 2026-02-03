from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('create/', views.create_view, name='create'),
    path('<int:pk>/', views.detail_view, name='detail'),
]