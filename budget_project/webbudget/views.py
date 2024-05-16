import datetime
from decimal import Decimal
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
    Func,
    Q,
    Subquery,
    OuterRef,
)
from django.db.models.functions import Round, Coalesce
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from pprint import pprint

from bot.models import (
    Currency,
    Money,
    Category,
    Rate,
    Type,
    UserMainCurrency,
)
from .filters import MoneyFilter
from .forms import CategoryForm, IncomeForm, UserMainCurrencyForm
from .graphic_creator import create_grafic, incomes_by_categories, expenses_by_categories

from django.http import JsonResponse
from django.core.serializers import serialize
import json

current_month = datetime.datetime.now().month

def all_money_with_value_in_main_currency(request, type):
    rate = Rate.objects.filter(
            date=OuterRef('date'),
            first_currency=OuterRef('current_first_currency'),
            second_currency=OuterRef('current_second_currency')
        )

    return Money.objects.filter(
        type__name=type,
        author=request.user
    ).annotate(
        current_first_currency=F('author__usermaincurrency__main_currency__id'),
        current_second_currency=F('currency__id'),
    ).annotate(
        value_in_main_currency=ExpressionWrapper(
            F('value') / Subquery(rate.values('rate')[:1]),
            output_field=FloatField()
        )
    ).order_by('date')
        


def categories(request, type):

    rate = Rate.objects.filter(
        date=OuterRef('date'),
        first_currency=OuterRef('current_first_currency'),
        second_currency=OuterRef('current_second_currency')
    )

    moneys = Money.objects.filter(
        date__month=current_month,
        author=request.user,
        category=OuterRef('id')
    ).annotate(
        current_first_currency=F('author__usermaincurrency__main_currency__id'),
        current_second_currency=F('currency__id'),
    ).annotate(
        value_in_main_currency=ExpressionWrapper(
            F('value') / Subquery(rate.values('rate')[:1]),
            output_field=FloatField()
        )
    ).annotate(
        total_value=Func('value_in_main_currency', function='Sum', output_field=FloatField())
    )

    categories = Category.objects.filter(
        type__name=type,
        author=request.user.id
    ).annotate(
        values_in_main_currency=Round(
            Subquery(
                moneys.values('total_value')
            ),
            2
        ),
    ).annotate(
        difference=Round(ExpressionWrapper(F('limit') - F('values_in_main_currency'), output_field=FloatField()), 2)
    ) # категории доходов
    print(categories.values())
    return categories


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
    print(categories_plan_sum['difference'])
    return categories_plan_sum

@login_required
def dashboard(request, pk=None):

    if pk is not None:
        instance = get_object_or_404(Money, pk=pk)

    else:
        instance = None


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
        current_first_currency=F('author__usermaincurrency__main_currency__id'),
        current_second_currency=F('currency__id'),
    ).annotate(
        value_in_main_currency=ExpressionWrapper(
            F('value') / Subquery(rate.values('rate')[:1]),
            output_field=FloatField()
        ),
    ).aggregate(
        sum_incomes_values = Round(Sum('value_in_main_currency', filter=Q(type__name='incomes')), 2),
        sum_expenses_values = Round(Sum('value_in_main_currency', filter=Q(type__name='expenses')), 2),
    )

    print('all')
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

    diff_plan_fact_incomes_values = (
        categories_plan_sum(request)['income_categories_sum']
        - all_incomes_with_sum['sum_incomes_values']
    )
    diff_plan_fact_expenses_values = (
        categories_plan_sum(request)['expense_categories_sum']
        - all_incomes_with_sum['sum_expenses_values']
    )
    diff_total_plan_fact_values = (
        diff_plan_fact_incomes_values
        - diff_plan_fact_expenses_values
    )

    filter = MoneyFilter(request.GET, queryset=all_incomes)

    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    main_currency = get_object_or_404(UserMainCurrency, author=request.user).main_currency

    create_grafic(request)
    incomes_by_categories(request)
    expenses_by_categories(request)

    instance = get_object_or_404(UserMainCurrency, author=request.user)
    set_currency_form = UserMainCurrencyForm(request.POST or None, instance=instance)

    context = {
        'title': title,
        'page_obj': page_obj,
        'categories': categories(request, type='incomes'),
        'expence_categories': categories(request, type='expenses'),
        'all_incomes_with_sum': all_incomes_with_sum,
        'diff_incomes_expenses_values': round(diff_incomes_expenses_values, 2),
        'diff_plan_fact_incomes_values': diff_plan_fact_incomes_values,
        'diff_plan_fact_expenses_values': diff_plan_fact_expenses_values,
        'diff_total_plan_fact_values': diff_total_plan_fact_values,
        'categories_plan_sum': categories_plan_sum(request),
        'main_currency': main_currency,
        'filter': filter,
        'username': request.user.username,
        'form': form,
        'set_currency_form': set_currency_form,
    }
    if set_currency_form.is_valid():
        set_currency_form.save()
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

    instance = get_object_or_404(UserMainCurrency, author=request.user)
    set_currency_form = UserMainCurrencyForm(request.POST or None, instance=instance)

    context = {
        'title': title,
        # 'products': products,
        'page_obj': page_obj,
        'categories': categories(request, type='incomes'),
        'expence_categories': categories(request, type='expenses'),
        'filter': filter,
        'form': form,
        'set_currency_form': set_currency_form,
    }
    if set_currency_form.is_valid():
        set_currency_form.save()

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

    instance = get_object_or_404(UserMainCurrency, author=request.user)
    set_currency_form = UserMainCurrencyForm(request.POST or None, instance=instance)

    title = 'Category'

    context = {
        'title': title,
        'categories': categories(request, type='incomes'),
        'expence_categories': categories(request, type='expenses'),
        'form': form,
        'set_currency_form': set_currency_form,
    }

    if set_currency_form.is_valid():
        set_currency_form.save()

    if request.method == 'POST':
        return redirect('webbudget:category')

    return render(request, 'webbudget/category.html', context)


@login_required
def delete_category(request, pk):
    instance = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=instance)

    instance = get_object_or_404(UserMainCurrency, author=request.user)
    set_currency_form = UserMainCurrencyForm(request.POST or None, instance=instance)

    title = 'Category'

    context = {
        'title': title,
        'categories': categories(request, type='incomes'),
        'expence_categories': categories(request, type='expenses'),
        'form': form,
        'set_currency_form': set_currency_form,
    }

    if set_currency_form.is_valid():
        set_currency_form.save()

    if request.method == 'POST':
        instance.delete()
        return redirect('webbudget:category')
    return render(request, 'webbudget/category.html', context)


@login_required
def main_currency(request):
    instance = get_object_or_404(UserMainCurrency, author=request.user)
    set_currency_form = UserMainCurrencyForm(request.POST or None, instance=instance)

    context = {
        'categories': categories(request, type='incomes'),
        'expence_categories': categories(request, type='expenses'),
        'main_currency': main_currency,
        'set_currency_form': set_currency_form
    }

    if set_currency_form.is_valid():
        set_currency_form.save()

    if request.method == 'POST':
        return redirect('webbudget:dashboard')

    return render(request, 'webbudget/dashboard.html', context)
