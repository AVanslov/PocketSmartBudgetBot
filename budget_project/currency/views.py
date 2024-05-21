from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Min, Sum, Max, IntegerField, ExpressionWrapper, F, Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from webbudget import forms 
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
    currencies = Rate.objects.filter(
        # date=today,
        # ~Q(rate=1)
    ).order_by('-date')
    graphic_creator.currencies_grafic(request)

    instance = get_object_or_404(UserMainCurrency, author=request.user)
    set_currency_form = forms.UserMainCurrencyForm(request.POST or None, instance=instance)

    title = 'Currencies rates'

    context = {
        'title': title,
        'main_currency': get_object_or_404(UserMainCurrency, author=request.user).main_currency,
        'currencies': currencies,
        'set_currency_form': set_currency_form,
    }
    if set_currency_form.is_valid():
        set_currency_form.save()
    return render(request, 'webbudget/currencies_rates.html', context)