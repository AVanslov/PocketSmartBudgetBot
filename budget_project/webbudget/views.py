import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import (
    Avg,
    Count,
    Min,
    Sum,
    Max,
    IntegerField,
    FloatField,
    ExpressionWrapper,
    F,
    Q,
    Subquery,
    OuterRef,
)
from django.db.models.functions import Round
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from pprint import pprint

from bot.models import (
    Currency,
    Money,
    Category,
    Rate,
    UserMainCurrency,
)
from .filters import MoneyFilter
from .forms import CategoryForm, IncomeForm, UserMainCurrencyForm
from .graphic_creator import create_grafic

from django.http import JsonResponse
from django.core.serializers import serialize
import json

current_month = datetime.datetime.now().month

def income_categories(request):

    sum_values_current_month = Sum('money__value', filter=Q(money__date__month=current_month))

    categories = Category.objects.filter(
        type__name='incomes',
        author=request.user.id
    ).annotate(
        sum_values=sum_values_current_month,
        difference=ExpressionWrapper(F('limit') - F('sum_values'), output_field=IntegerField())
    ) # категории доходов
    return categories

def expence_categories(request):
    sum_values_current_month = Sum('money__value', filter=Q(money__date__month=current_month))

    expence_categories = Category.objects.filter(
        type__name='expenses',
        author=request.user.id
    ).annotate(
        sum_values=sum_values_current_month,
        difference=ExpressionWrapper(F('limit') - F('sum_values'), output_field=IntegerField())
    ) # категории расходов
    return expence_categories

def categories_plan_sum(request):
    sum_income_values_current_month = Sum('limit', filter=Q(type__name='incomes'))
    sum_expense_values_current_month = Sum('limit', filter=Q(type__name='expenses'))

    categories_plan_sum = Category.objects.filter(
        author=request.user.id
    ).aggregate(
        income_categories_sum = sum_income_values_current_month,
        expense_categories_sum = sum_expense_values_current_month,
        difference=sum_income_values_current_month - sum_expense_values_current_month
    )
    # print([i.incomes_sum for i in income_categories_plan_sum])
    print(categories_plan_sum['difference'])
    return categories_plan_sum

@login_required
def dashboard(request, pk=None):

    if pk is not None:
        instance = get_object_or_404(Money, pk=pk)

    else:
        instance = None

    # kwargs = {
    #     'request': request
    #     }
    # kwargs.update({'request': request}) # usually with conditionals to specify what gets added


    form = IncomeForm(request.POST or None, instance=instance, initial={'request': request.user})

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        form.save()

    title = 'Dashboard'

    all_incomes = Money.objects.filter(
        author=request.user
    ).order_by('-date')


    rate = Rate.objects.filter(
        date=OuterRef('date'),
        first_currency=OuterRef('current_first_currency'),
        second_currency=OuterRef('current_second_currency')
    )

    all_incomes_with_sum = Money.objects.filter(
        author=request.user
    ).annotate(
        current_first_currency=F('currency__id'),
        current_second_currency=F('author__usermaincurrency__main_currency__id'),
    ).annotate(
        value_in_main_currency=ExpressionWrapper(
            F('value') / Subquery(rate.values('rate')[:1]),
            output_field=FloatField()
        )
    ).aggregate(
        sum_incomes_values = Round(Sum('value_in_main_currency', filter=Q(type__name='incomes')), 2),
        sum_expenses_values = Round(Sum('value_in_main_currency', filter=Q(type__name='expenses')), 2),
    )

    pprint(all_incomes_with_sum)
    pprint(type(all_incomes_with_sum['sum_incomes_values']))
    pprint(type(all_incomes_with_sum['sum_expenses_values']))

    if type(all_incomes_with_sum['sum_incomes_values']) is not float or type(all_incomes_with_sum['sum_expenses_values']) is not float:
        if type(all_incomes_with_sum['sum_incomes_values']) is float and type(all_incomes_with_sum['sum_expenses_values']) is not float:
            diff_incomes_expenses_values = all_incomes_with_sum['sum_incomes_values']
        if type(all_incomes_with_sum['sum_incomes_values']) is not float and type(all_incomes_with_sum['sum_expenses_values']) is float:
            diff_incomes_expenses_values = 0 - all_incomes_with_sum['sum_expenses_values']
        else:
            diff_incomes_expenses_values = 0
    else:
        diff_incomes_expenses_values = (
            all_incomes_with_sum['sum_incomes_values'] -
            all_incomes_with_sum['sum_expenses_values']
        )

    filter = MoneyFilter(request.GET, queryset=all_incomes)

    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    main_currency = get_object_or_404(UserMainCurrency, author=request.user).main_currency

    create_grafic(request)
    context = {
        'title': title,
        'page_obj': page_obj,
        'categories': income_categories(request),
        'expence_categories': expence_categories(request),
        'all_incomes_with_sum': all_incomes_with_sum,
        'diff_incomes_expenses_values': diff_incomes_expenses_values,
        'categories_plan_sum': categories_plan_sum(request),
        'main_currency': main_currency,
        'filter': filter,
        'form': form
    }
    if request.method == 'POST':
        return redirect('webbudget:dashboard')
    return render(request, 'webbudget/dashboard.html', context)


@login_required
def delete_money(request, pk):
    instance = get_object_or_404(Money, pk=pk)
    form = IncomeForm(instance=instance, initial={'request': request.user})
    
    title = 'Dashboard'
    all_incomes = Money.objects.filter(author=request.user).order_by('-date')

    filter = MoneyFilter(request.GET, queryset=all_incomes)

    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': title,
        # 'products': products,
        'page_obj': page_obj,
        'categories': income_categories(request),
        'expence_categories': expence_categories(request),
        'filter': filter,
        'form': form
    }

    if request.method == 'POST':
        instance.delete()
        return redirect('webbudget:dashboard')
    return render(request, 'webbudget/dashboard.html', context)


@login_required
def edit_category(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Category, pk=pk)

    else:
        instance = None

    form = CategoryForm(request.POST or None, instance=instance)
    
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        form.save()

    context = {
        'categories': income_categories(request),
        'expence_categories': expence_categories(request),
        'form': form
    }
    if request.method == 'POST':
        return redirect('webbudget:category')

    return render(request, 'webbudget/category.html', context)


@login_required
def delete_category(request, pk):
    instance = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=instance)

    context = {
        'categories': income_categories(request),
        'expence_categories': expence_categories(request),
        'form': form
    }

    if request.method == 'POST':
        instance.delete()
        return redirect('webbudget:category')
    return render(request, 'webbudget/category.html', context)


@login_required
def main_currency(request):
    instance = get_object_or_404(UserMainCurrency, author=request.user)
    form = UserMainCurrencyForm(request.POST or None, instance=instance)

    context = {
        'categories': income_categories(request),
        'expence_categories': expence_categories(request),
        'main_currency': main_currency,
        'form': form
    }

    if form.is_valid():
        form.save()

    if request.method == 'POST':
        return redirect('webbudget:dashboard')

    return render(request, 'webbudget/category.html', context)
