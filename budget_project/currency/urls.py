from django.urls import include, path
from . import views

app_name = 'currency'


urlpatterns = [
    path('currencies-rates/', views.currencies_rates, name='currencies_rates'),
]
