from django.conf import settings
from django.shortcuts import get_object_or_404
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import datetime

from bot.models import Currency, Money, Rate, UserMainCurrency
from . import views

CURRENT_MONTH = datetime.datetime.now().month
CURRENT_YEAR = datetime.datetime.now().year

BACKGROUND_COLOR = '#f2f2f2'

def currencies_grafic(request):
    """
    Выводит график по стоимости всех валют относительно EUR.
    """
    name = 'currencies.png'
    name_of_file =  settings.MEDIA_ROOT / name

    print('!!!')
    print('URL')
    print(name_of_file)
    print('URL')

    # currencies_list = [i.name for i in Currency.objects.all()]

    data = [[rate.rate for rate in Rate.objects.filter(date__year=CURRENT_YEAR , first_currency__name=request.user.usermaincurrency.main_currency.name, second_currency__name=i.name).order_by('date')] for i in Currency.objects.all()]
    dates = [[rate.date for rate in Rate.objects.filter(date__year=CURRENT_YEAR ,first_currency__name=request.user.usermaincurrency.main_currency.name, second_currency__name=i.name).order_by('date')] for i in Currency.objects.all()]
    labels = [[rate.second_currency.name for rate in Rate.objects.filter(date__year=CURRENT_YEAR , first_currency__name=request.user.usermaincurrency.main_currency.name, second_currency__name=i.name).order_by('date')] for i in Currency.objects.all()]

    fig = plt.figure(facecolor=BACKGROUND_COLOR, figsize=(15, 3))
    # plt.axes().set_facecolor(BACKGROUND_COLOR)
    ax = fig.add_subplot(1, 1, 1)
    for i, pair in enumerate(data, 0):
        if len(dates[i]) != 0:
            print(len(dates[i]))
            print(len(pair))
            ax.plot(dates[i], pair, label=str(labels[i][0]))
            ax.set_facecolor(BACKGROUND_COLOR)
    
    ax.set_title("Currencies")
    ax.legend()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    fig.tight_layout()

    plt.savefig(name_of_file)
    file_with_grafics = open(name_of_file, 'rb')
    plt.close()
    return file_with_grafics



def incomes_by_categories(request):
    name = str(request.user.username) + '_income_categories.png'
    name_of_file =  settings.MEDIA_ROOT / name

    data = [category.values_in_main_currency for category in views.categories(request, type='incomes') if category.values_in_main_currency is not None]
    categories_name = [category.category for category in views.categories(request, type='incomes') if category.values_in_main_currency is not None]

    fig, ax = plt.subplots(figsize=(5, 3), subplot_kw=dict(aspect="equal"),facecolor=BACKGROUND_COLOR)

    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d} {get_object_or_404(UserMainCurrency, author=request.user).main_currency.name})"
    
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(data)))

    wedges, texts, autotexts  = ax.pie(
        data,
        labels=categories_name,
        autopct=lambda pct: func(pct, data),
        # textprops=dict(color="w"),
        colors=colors,
        wedgeprops={"linewidth": 1, "edgecolor": "white"}
    )

    plt.setp(autotexts, size=7, weight="bold")

    # ax.set_title("Income Categories")

    plt.savefig(name_of_file)
    file_with_grafics = open(name_of_file, 'rb')
    plt.close()
    return file_with_grafics


def expenses_by_categories(request):
    name = str(request.user.username) + '_expense_categories.png'
    name_of_file =  settings.MEDIA_ROOT / name

    data = [category.values_in_main_currency for category in views.categories(request, type='expenses') if category.values_in_main_currency is not None]
    categories_name = [category.category for category in views.categories(request, type='expenses') if category.values_in_main_currency is not None]

    fig, ax = plt.subplots(figsize=(5, 3), subplot_kw=dict(aspect="equal"),facecolor=BACKGROUND_COLOR)

    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d} {get_object_or_404(UserMainCurrency, author=request.user).main_currency.name})"
    
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(data)))

    wedges, texts, autotexts  = ax.pie(
        data,
        labels=categories_name,
        autopct=lambda pct: func(pct, data),
        # textprops=dict(color="#CEE741"),
        colors=colors,
        wedgeprops={"linewidth": 1, "edgecolor": "white"}
    )

    plt.setp(autotexts, size=7, weight="bold")

    plt.savefig(name_of_file)
    file_with_grafics = open(name_of_file, 'rb')
    plt.close()
    return file_with_grafics


def incomes_or_expenses_grafic(incomes_object_dictinaries, name_of_file, request):
    dates = set(
            i['date'].strftime("%Y-%m")
            for i in incomes_object_dictinaries
        )
    grouped_expenses = [
        (date, [
            i['value_in_main_currency'] for i in incomes_object_dictinaries
            if i['date'].strftime("%Y-%m") == date
        ]) for date in dates
    ]
    summed_expenses = [
        {
            'date': k,
            'value_in_main_currency': sum(v)
        } for k, v in grouped_expenses
    ]
    xs_dates = [obj['date'] for obj in summed_expenses]
    ys_values = [obj['value_in_main_currency'] for obj in summed_expenses]


    # столбчатый график
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Tahoma', 'DejaVu Sans',
                            'Lucida Grande', 'Verdana']
    plt.figure(facecolor=BACKGROUND_COLOR, figsize=(10, 2))
    plt.axes().set_facecolor(BACKGROUND_COLOR)

    # plt.subplot(2, 1, 1)
    plt.bar(
        xs_dates,
        ys_values,
        label='Incomes',
        color='#CEE741',
    )

    plt.xlabel('Month')
    plt.ylabel('Income, in {}'.format(request.user.usermaincurrency.main_currency.name))
    plt.title('Incomes by months')
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig(name_of_file)
    file_with_grafics = open(name_of_file, 'rb')
    plt.close()
    return file_with_grafics


def incomes_and_expenses_grafic(incomes_object_dictinaries, expenses_object_dictinaries, name_of_file, request):
    # получить даты из доходов
    incomes_dates = [i['date'] for i in incomes_object_dictinaries]
    # получить даты из расходов
    expenses_dates = [i['date'] for i in expenses_object_dictinaries]
    # объединить списки
    incomes_dates.extend(expenses_dates)
    # отсортировать списки
    incomes_dates.sort()
    # преобразовать элементы в строку
    # превратить в множество
    dates = set([i.strftime("%Y-%m") for i in incomes_dates])
    grouped = [
        (date, [
            round(i['value_in_main_currency'], 1) for i in incomes_object_dictinaries
            if i['date'].strftime("%Y-%m") == date
        ]) for date in dates
    ]
    
    grouped_expenses = [
        (date, [
            round(i['value_in_main_currency'], 1) for i in expenses_object_dictinaries
            if i['date'].strftime("%Y-%m") == date
        ]) for date in dates
    ]


    current_year_monthes = [datetime.datetime(int(CURRENT_YEAR), i, 1).strftime("%Y-%m") for i in range(1,13)]

    default_values_for_current_year = [(month, [0]) for month in current_year_monthes]


    print('!!!')
    print (current_year_monthes)
    print (grouped)

    dates_with_incomes_values = [i[0] for i in grouped]
    dates_with_expenses_values = [i[0] for i in grouped_expenses]

    for i in default_values_for_current_year:
        if i[0] not in dates_with_incomes_values:
            grouped.append(i)
        if i[0] not in dates_with_expenses_values:
            grouped_expenses.append(i)

    grouped.sort(key=lambda x: x[0])
    grouped_expenses.sort(key=lambda x: x[0])

    print('!!!')
    print (grouped)
    print (grouped_expenses)

    
    # отфильтровать все даты по текущему году
    # выстроить даты в порядке позрастания
    # если месяц пропущен, добавить его и добавить значения 0, 0
    # можно загатовить список с значениями по умолчанию и объеденить его со списком полученных данных - тогда будет только 12 столбцов

    

    summed = [
        {
            'date': k,
            'value_in_main_currency': sum(v)
        } for k, v in grouped
    ]
    xs_dates = [obj['date'] for obj in summed]
    ys_values = [obj['value_in_main_currency'] for obj in summed]
    expenses_summed = [
        {
            'date': k,
            'value_in_main_currency': sum(v)
        } for k, v in grouped_expenses
    ]
    ys_expenses_values = [obj['value_in_main_currency'] for obj in expenses_summed]
    x = np.arange(len(xs_dates))  # the label locations
    width = 0.35  # the width of the bars

    # plt.axes().set_facecolor(BACKGROUND_COLOR)
    # plt.figure(facecolor=BACKGROUND_COLOR, figsize=(10, 2))

    fig, ax = plt.subplots(facecolor=BACKGROUND_COLOR, figsize=(15, 3))
    rects1 = ax.bar(x - width/2, ys_values, width, label='Incomes', color='#CEE741')
    rects2 = ax.bar(x + width/2, ys_expenses_values, width, label='Expenses', color='#e75441')
    
    ax.set_facecolor(BACKGROUND_COLOR)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('{}'.format(request.user.usermaincurrency.main_currency.name))
    # ax.set_title('Incomes and expenses, in {}'.format(request.user.usermaincurrency.main_currency.name))
    ax.set_xticks(x, xs_dates)
    ax.legend()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.savefig(name_of_file)
    file_with_grafics = open(name_of_file, 'rb')
    plt.close()
    return file_with_grafics


def create_grafic(request):
    """
    Создает графики на основе объекта запроса.
    """


    incomes_object_dictinaries = [money for money in views.all_money_with_value_in_main_currency(request, type='incomes').values()]
    expenses_object_dictinaries = [money for money in views.all_money_with_value_in_main_currency(request, type='expenses').values()]
    print('error')
    print(incomes_object_dictinaries)

    name = str(request.user.username) + '_incomes_expenses.png'
    name_of_file =  settings.MEDIA_ROOT / name

    print('!!!')
    print('URL')
    print(name_of_file)
    print('URL')

    ### !!! Ошибка при создании графика, если у пользователя есть только расходы за несколько разных месяцев, а доходов нет
    return incomes_and_expenses_grafic(incomes_object_dictinaries, expenses_object_dictinaries, name_of_file, request)
    # if incomes_object_dictinaries and not expenses_object_dictinaries:
    #     # return incomes_or_expenses_grafic(incomes_object_dictinaries, name_of_file, request)
    # if expenses_object_dictinaries and not incomes_object_dictinaries:
    #     # return incomes_or_expenses_grafic(expenses_object_dictinaries,name_of_file, request)
    #     return incomes_and_expenses_grafic(incomes_object_dictinaries, expenses_object_dictinaries, name_of_file, request)
    # if incomes_object_dictinaries and expenses_object_dictinaries:
    #     return incomes_and_expenses_grafic(incomes_object_dictinaries, expenses_object_dictinaries, name_of_file, request)
    # else:
    #     return currencies_grafic(request)
