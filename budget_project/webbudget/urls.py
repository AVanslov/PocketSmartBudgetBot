from django.urls import include, path
from . import views

app_name = 'webbudget'


urlpatterns = [
    # path('<username>/dashboard/', views.dashboard),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:pk>/edit/', views.dashboard, name='edit'),
    path('dashboard/<int:pk>/delete/', views.delete_money, name='delete'),
]
