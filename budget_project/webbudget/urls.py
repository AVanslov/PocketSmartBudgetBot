from django.urls import include, path
from . import views

app_name = 'webbudget'


urlpatterns = [
    # path('<username>/dashboard/', views.dashboard),
    path('dashboard/', views.dashboard, name='dashboard'),
]
