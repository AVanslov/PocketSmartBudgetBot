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
    Value,
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
current_year = datetime.datetime.now().year

def all_money_with_value_in_main_currency(request, type):
    """
    Return user`s money objects in user`s main currency.
    """

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
    """
    Return the user's categories with the total value in the user's primary currency
    for each category, as
    well as the difference between the limit set by each user
    for the category and the actual income and expenses.
    """

    rate = Rate.objects.filter(
        date=OuterRef('date'), # Получаем дату текущего родительского объекта
        first_currency=OuterRef('current_first_currency'), # Получаем первую валюту в паре (она же главная валюта пользователя) текущего родительского объекта
        second_currency=OuterRef('current_second_currency') # Получаем вторую валюту в паре (она же валюта родительского объекта модели Money)
    )
    print('month')
    print(current_month)
    moneys = Money.objects.filter(
        # date__month=current_month,
        date__year=current_year,
        author=request.user,
        # Говорим, что ID категории смотреть в родительском Queryset
        category=OuterRef('id')
    ).annotate(
        # Получаем id объекта главной валюты
        current_first_currency=F('author__usermaincurrency__main_currency__id'),
        # Получаем id объекта валюты текущей денежной операции
        current_second_currency=F('currency__id'),
    ).annotate(
        # Вычисляем величину в эквиваленте главной валюты,
        # исходя из курса валют, который был в указанную дату этой денежной операции
        value_in_main_currency=ExpressionWrapper(
            F('value') / Subquery(rate.values('rate')[:1]),
            output_field=FloatField(),
            # filter=Q(date__mounth=current_month)
        ),
    ).annotate(
        total_value=Coalesce(Sum('value_in_main_currency'), Value(0), output_field=FloatField()),
        jan=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=1)), Value(0), output_field=FloatField()),
        feb=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=2)), Value(0), output_field=FloatField()),
        mar=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=3)), Value(0), output_field=FloatField()),
        apr=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=4)), Value(0), output_field=FloatField()),
        may=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=5)), Value(0), output_field=FloatField()),
        jun=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=6)), Value(0), output_field=FloatField()),
        jul=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=7)), Value(0), output_field=FloatField()),
        aug=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=8)), Value(0), output_field=FloatField()),
        sep=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=9)), Value(0), output_field=FloatField()),
        oct=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=10)), Value(0), output_field=FloatField()),
        nov=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=11)), Value(0), output_field=FloatField()),
        dec=Coalesce(Sum('value_in_main_currency', filter=Q(date__month=12)), Value(0), output_field=FloatField()),
    # ).annotate(
        # Получаем сумму всех денежных операций в текущей категории за текущий месяц
        # total_value=Func(
        #     'value_in_main_currency',
        #     function='Sum',
        #     output_field=FloatField(),
        # ),
        # jan=Func(
        #     'value_in_main_currency',
        #     function='Sum',
        #     output_field=FloatField(),
        # ),
    )

    categories = Category.objects.filter(
        type__name=type,
        author=request.user.id
    ).annotate(
        # Получаем дочерний Queryset и берем из него только аннотированное значение суммы денежный операций в текущей категории,
        # поскольку аннотаций добавляет значение к каждому объекту модели,
        # в Subquery передаются по очереди все ID категорий и попадают по очереди в OuterRef('id')
        values_in_main_currency=Round(
            Subquery(
                moneys.values('total_value')
            ),
            2
        ),
        jan=Round(Subquery(moneys.values('jan')), 2),
        feb=Round(Subquery(moneys.values('feb')), 2),
        mar=Round(Subquery(moneys.values('mar')), 2),
        apr=Round(Subquery(moneys.values('apr')), 2),
        may=Round(Subquery(moneys.values('may')), 2),
        jun=Round(Subquery(moneys.values('jun')), 2),
        jul=Round(Subquery(moneys.values('jul')), 2),
        aug=Round(Subquery(moneys.values('aug')), 2),
        sep=Round(Subquery(moneys.values('sep')), 2),
        oct=Round(Subquery(moneys.values('oct')), 2),
        nov=Round(Subquery(moneys.values('nov')), 2),
        dec=Round(Subquery(moneys.values('dec')), 2),
    ).annotate(
        difference=Round(ExpressionWrapper(F('limit') - F('values_in_main_currency'), output_field=FloatField()), 2),
    ) # категории доходов
    # print(categories.values())
    return categories


def categories_by_monthes_aggrigations(request, type):
    rate = Rate.objects.filter(
        date=OuterRef('date'), # Получаем дату текущего родительского объекта
        first_currency=OuterRef('current_first_currency'), # Получаем первую валюту в паре (она же главная валюта пользователя) текущего родительского объекта
        second_currency=OuterRef('current_second_currency') # Получаем вторую валюту в паре (она же валюта родительского объекта модели Money)
    )

    moneys = Money.objects.filter(
        type__name=type,
        # date__month=current_month,
        date__year=current_year,
        author=request.user,
        # category=OuterRef('id'),
    ).annotate(
        # Получаем id объекта главной валюты
        current_first_currency=F('author__usermaincurrency__main_currency__id'),
        # Получаем id объекта валюты текущей денежной операции
        current_second_currency=F('currency__id'),
    ).annotate(
        # Вычисляем величину в эквиваленте главной валюты,
        # исходя из курса валют, который был в указанную дату этой денежной операции
        value_in_main_currency=ExpressionWrapper(
            F('value') / Subquery(rate.values('rate')[:1]),
            output_field=FloatField(),
        ),
    ).aggregate(
        total_value_jan=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=1)), Value(0), output_field=FloatField()), 2),
        total_value_feb=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=2)), Value(0), output_field=FloatField()), 2),
        total_value_mar=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=3)), Value(0), output_field=FloatField()), 2),
        total_value_apr=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=4)), Value(0), output_field=FloatField()), 2),
        total_value_may=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=5)), Value(0), output_field=FloatField()), 2),
        total_value_jun=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=6)), Value(0), output_field=FloatField()), 2),
        total_value_jul=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=7)), Value(0), output_field=FloatField()), 2),
        total_value_aug=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=8)), Value(0), output_field=FloatField()), 2),
        total_value_sep=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=9)), Value(0), output_field=FloatField()), 2),
        total_value_oct=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=10)), Value(0), output_field=FloatField()), 2),
        total_value_nov=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=11)), Value(0), output_field=FloatField()), 2),
        total_value_dec=Round(Coalesce(Sum('value_in_main_currency', filter=Q(date__month=12)), Value(0), output_field=FloatField()), 2),
    )
    return moneys

def categories_plan_sum(request):
    """
    Return user`s ctegories with limits set each category
    and difference between income`s limit and expense`s limit values.
    """

    sum_income_values_current_month = Sum('limit', filter=Q(type__name='incomes'))
    sum_expense_values_current_month = Sum('limit', filter=Q(type__name='expenses'))

    categories_plan_sum = Category.objects.filter(
        author=request.user.id
    ).aggregate(
        income_categories_sum = sum_income_values_current_month,
        expense_categories_sum = sum_expense_values_current_month,
        difference=sum_income_values_current_month - sum_expense_values_current_month
    )
    # print(categories_plan_sum['difference'])
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
        author=request.user,
        date__month=current_month
    ).annotate(
        current_first_currency=F('author__usermaincurrency__main_currency__id'),
        current_second_currency=F('currency__id'),
    ).annotate(
        value_in_main_currency=ExpressionWrapper(
            F('value') / Subquery(rate.values('rate')[:1]),
            output_field=FloatField()
        ),
    ).aggregate(
        sum_incomes_values = Round(Coalesce(Sum('value_in_main_currency', filter=Q(type__name='incomes')), Value(0), output_field=FloatField()), 2),
        sum_expenses_values = Round(Coalesce(Sum('value_in_main_currency', filter=Q(type__name='expenses')), Value(0), output_field=FloatField()), 2),
    )

    # print('all')
    pprint(all_incomes_with_sum)
    # pprint(type(all_incomes_with_sum['sum_incomes_values']))
    # pprint(type(all_incomes_with_sum['sum_expenses_values']))

    # if type(all_incomes_with_sum['sum_incomes_values']) is not float or type(all_incomes_with_sum['sum_expenses_values']) is not float:
    #     if type(all_incomes_with_sum['sum_incomes_values']) is float and type(all_incomes_with_sum['sum_expenses_values']) is not float:
    #         diff_incomes_expenses_values = all_incomes_with_sum['sum_incomes_values']
    #     if type(all_incomes_with_sum['sum_incomes_values']) is not float and type(all_incomes_with_sum['sum_expenses_values']) is float:
    #         diff_incomes_expenses_values = 0 - all_incomes_with_sum['sum_expenses_values']
    #     else:
    #         diff_incomes_expenses_values = 0
    # else:
    diff_incomes_expenses_values = (
        all_incomes_with_sum['sum_incomes_values'] -
        all_incomes_with_sum['sum_expenses_values']
    )

    planning_incomes_sum = categories_plan_sum(request)['income_categories_sum']
    fact_incomes_sum = all_incomes_with_sum['sum_incomes_values']
    planning_expenses_sum = categories_plan_sum(request)['expense_categories_sum']
    fact_expenses_sum = all_incomes_with_sum['sum_expenses_values']

    # if categories_plan_sum(request)['income_categories_sum'] is None:
    #     planning_incomes_sum = 0

    # if all_incomes_with_sum['sum_incomes_values'] is None:
    #     fact_incomes_sum = 0

    # if categories_plan_sum(request)['expense_categories_sum'] is None:
    #     planning_expenses_sum = 0
    
    # if all_incomes_with_sum['sum_expenses_values'] is None:
    #     fact_expenses_sum = 0
        
    diff_plan_fact_incomes_values = round((
        planning_incomes_sum
        - fact_incomes_sum
    ), 2)
    diff_plan_fact_expenses_values = round((
        planning_expenses_sum
        - fact_expenses_sum
    ), 2)
    diff_total_plan_fact_values = round((
        diff_plan_fact_incomes_values
        - diff_plan_fact_expenses_values
    ), 2)

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

    # instance = get_object_or_404(UserMainCurrency, author=request.user)
    # set_currency_form = UserMainCurrencyForm(request.POST or None, instance=instance)

    context = {
        'title': title,
        # 'products': products,
        'main_currency': get_object_or_404(UserMainCurrency, author=request.user).main_currency,
        'page_obj': page_obj,
        'categories': categories(request, type='incomes'),
        'expence_categories': categories(request, type='expenses'),
        'filter': filter,
        'form': form,
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

    title = 'Category'

    dict=categories_by_monthes_aggrigations(request, type='incomes')
    expenses=categories_by_monthes_aggrigations(request, type='expenses')

    differenses = {number: round(dict[month] - expenses[month], 2) for number, month in enumerate(dict.keys(), 1)}

    context = {
        'title': title,
        'main_currency': get_object_or_404(UserMainCurrency, author=request.user).main_currency,
        'categories': categories(request, type='incomes'),
        'expence_categories': categories(request, type='expenses'),
        'total_income_values_of_categories': categories_by_monthes_aggrigations(request, type='incomes'),
        'total_incomes': sum(categories_by_monthes_aggrigations(request, type='incomes').values()),
        'total_expense_values_of_categories': categories_by_monthes_aggrigations(request, type='expenses'),
        'total_expenses': sum(categories_by_monthes_aggrigations(request, type='expenses').values()),
        'differenses': differenses,
        'total_value_of_year': round(sum(differenses.values()), 2),
        'form': form,
    }

    if request.method == 'POST':
        return redirect('webbudget:category')

    return render(request, 'webbudget/category.html', context)


@login_required
def delete_category(request, pk):
    instance = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=instance)

    # instance = get_object_or_404(UserMainCurrency, author=request.user)
    # set_currency_form = UserMainCurrencyForm(request.POST or None, instance=instance)

    title = 'Category'

    context = {
        'title': title,
        'main_currency': get_object_or_404(UserMainCurrency, author=request.user).main_currency,
        'categories': categories(request, type='incomes'),
        'expence_categories': categories(request, type='expenses'),
        'form': form,
        # 'set_currency_form': set_currency_form,
    }

    # if set_currency_form.is_valid():
    #     set_currency_form.save()

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
        'main_currency': get_object_or_404(UserMainCurrency, author=request.user).main_currency,
        'set_currency_form': set_currency_form
    }

    if set_currency_form.is_valid():
        set_currency_form.save()

    if request.method == 'POST':
        return redirect('webbudget:dashboard')

    return render(request, 'webbudget/dashboard.html', context)
