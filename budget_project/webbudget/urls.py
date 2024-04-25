from django.urls import include, path
from . import views

urlpatterns = [
    path('<username>/dashboard/', views.dashboard),
]
