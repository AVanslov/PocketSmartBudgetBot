from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from bot.models import (
    Money,
    Category,

)
from .filters import MoneyFilter
from .forms import IncomeForm
from .graphic_creator import create_grafic


@login_required
def dashboard(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Money, pk=pk)

    else:
        instance = None

    form = IncomeForm(request.POST or None, instance=instance)
    
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        form.save()

    title = 'Dashboard'
    all_incomes = Money.objects.filter(author=request.user).order_by('-date')

    filter = MoneyFilter(request.GET, queryset=all_incomes)

    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(type__name='incomes') # категории доходов
    expence_categories = Category.objects.filter(type__name='expenses') # категории расходов
    # categories = Category.objects.filter(type__name='incomes', author=request.user) # категории доходов
    # expence_categories = Category.objects.filter(type__name='expenses', author=request.user) # категории расходов
    create_grafic(request)
    context = {
        'title': title,
        'page_obj': page_obj,
        'categories': categories,
        'expence_categories': expence_categories,
        'filter': filter,
        'form': form
    }
    return render(request, 'webbudget/dashboard.html', context)


def delete_money(request, pk):
    instance = get_object_or_404(Money, pk=pk)
    form = IncomeForm(instance=instance)
    
    title = 'Dashboard'
    all_incomes = Money.objects.filter(author=request.user).order_by('-date')

    filter = MoneyFilter(request.GET, queryset=all_incomes)

    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(type__name='incomes', author=request.user) # категории доходов
    expence_categories = Category.objects.filter(type__name='expenses', author=request.user) # категории расходов

    context = {
        'title': title,
        # 'products': products,
        'page_obj': page_obj,
        'categories': categories,
        'expence_categories': expence_categories,
        'filter': filter,
        'form': form
    }

    if request.method == 'POST':
        instance.delete()
        return redirect('webbudget:dashboard')
    return render(request, 'webbudget/dashboard.html', context)
