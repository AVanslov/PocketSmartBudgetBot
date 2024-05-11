from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Min, Sum, Max, IntegerField, ExpressionWrapper, F, Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from bot.models import (
    Money,
    Category,
    Rate,
    UserMainCurrency,
)
from webbudget import graphic_creator

today = date.today()

@login_required
def currencies_rates(request):
    currencies = Rate.objects.filter(date=today)
    graphic_creator.currencies_grafic()
    context = {
        'currencies': currencies
    }
    return render(request, 'webbudget/currencies_rates.html', context)