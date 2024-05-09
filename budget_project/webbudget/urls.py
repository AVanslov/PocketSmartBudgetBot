from django.urls import include, path
from . import views

app_name = 'webbudget'


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('category/', views.edit_category, name='category'),
    path('category/<int:pk>/edit/', views.edit_category, name='category_edit'),
    path('category/<int:pk>/delete/', views.delete_category, name='category_delete'),
    path('dashboard/<int:pk>/edit/', views.dashboard, name='edit'),
    path('dashboard/<int:pk>/delete/', views.delete_money, name='delete'),
    path('set-main-currency/', views.main_currency, name='currency'),
]
