from django.conf import settings
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime

from bot.models import Money
from . import views

current_month = datetime.datetime.now().month


def incomes_by_categories(request):
    name = str(request.user.username) + '_categories.png'
    name_of_file =  settings.MEDIA_ROOT / name

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    print(f'value_in_main_currency {Money.objects.get(id=1).value_in_main_currency}')

    # Money.objects.filter(author=request.user, date)
    categories = []

    recipe = ["375 g flour","75 g sugar","250 g butter","300 g berries"]

    data = [float(x.split()[0]) for x in recipe]
    ingredients = [x.split()[-1] for x in recipe]


    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d} g)"


    wedges, texts, autotexts = ax.pie(
        data,
        autopct=lambda pct: func(pct, data),
        textprops=dict(color="w")
    )

    ax.legend(wedges, ingredients,
            title="Ingredients",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("Matplotlib bakery: A pie")

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
    plt.figure(facecolor='#f2f2f2', figsize=(10, 2))
    plt.axes().set_facecolor('#f2f2f2')

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

    # plt.subplot(2, 1, 2)
    # plt.bar(
    #     xs_dates,
    #     ys_values,
    #     label='Incomes',
    #     color='#CEE741',
    # )
    # plt.xlabel('Month')
    # plt.ylabel('Income, in {}'.format(request.user.usermaincurrency.main_currency.name))
    # plt.title('Incomes by months')
    # for spine in plt.gca().spines.values():
    #     spine.set_visible(False)


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
            i['value_in_main_currency'] for i in incomes_object_dictinaries
            if i['date'].strftime("%Y-%m") == date
        ]) for date in dates
    ]
    grouped_expenses = [
        (date, [
            i['value_in_main_currency'] for i in expenses_object_dictinaries
            if i['date'].strftime("%Y-%m") == date
        ]) for date in dates
    ]

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

    # plt.axes().set_facecolor('#f2f2f2')
    # plt.figure(facecolor='#f2f2f2', figsize=(10, 2))

    fig, ax = plt.subplots(facecolor='#f2f2f2', figsize=(5, 3))
    rects1 = ax.bar(x - width/2, ys_values, width, label='Incomes', color='#CEE741')
    rects2 = ax.bar(x + width/2, ys_expenses_values, width, label='Expenses', color='#e75441')
    
    ax.set_facecolor('#f2f2f2')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('{}'.format(request.user.usermaincurrency.main_currency.name))
    ax.set_title('Incomes and expenses, in {}'.format(request.user.usermaincurrency.main_currency.name))
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
    name = str(request.user.username) + '_incomes_expenses.png'
    name_of_file =  settings.MEDIA_ROOT / name
    if incomes_object_dictinaries and not expenses_object_dictinaries:
        return incomes_or_expenses_grafic(incomes_object_dictinaries, name_of_file, request)
    if expenses_object_dictinaries and not incomes_object_dictinaries:
        return incomes_or_expenses_grafic(expenses_object_dictinaries, name_of_file, request)
    if incomes_object_dictinaries and expenses_object_dictinaries:
        return incomes_and_expenses_grafic(incomes_object_dictinaries, expenses_object_dictinaries, name_of_file, request)


# def create_grafic(chat, group_by: str, value_for_sum: str, type: str = 'bar'):
#     """
#     Создает график на основе списка словарей
#     - каждый словарь
#     - объект таблицы Income
#     - группирует значения value по датам
#     - возвращает закодированное в base 64 изображение графика.
#     """
#     expenses_object_dictinaries = views.get_report_expenses(chat)

#     object_dictinaries = views.get_report(chat)
#     if len(object_dictinaries) == 0 and len(expenses_object_dictinaries) == 0:
#         name_of_file = './media/add_some_data.png'
#         file_without_grofics = open(name_of_file, 'rb')
#         return file_without_grofics
#     elif len(object_dictinaries) == 0 and len(expenses_object_dictinaries) > 0:
#         name_of_file = './media/grafics/' + str(chat.id) + 'expenses_by_' + group_by + '.png'
#         if os.path.exists(name_of_file):
#             os.remove(name_of_file)
#         dates = set(
#                 i[group_by].strftime("%Y-%m")
#                 for i in expenses_object_dictinaries
#             )
#         grouped_expenses = [
#             (date, [
#                 i[value_for_sum] for i in expenses_object_dictinaries
#                 if i[group_by].strftime("%Y-%m") == date
#             ]) for date in dates
#         ]
#         summed_expenses = [
#             {
#                 group_by: k,
#                 value_for_sum: sum(v)
#             } for k, v in grouped_expenses
#         ]
#         xs_dates = [obj[group_by] for obj in summed_expenses]
#         ys_values = [obj[value_for_sum] for obj in summed_expenses]
#         # столбчатый график
#         plt.bar(
#             xs_dates,
#             ys_values,
#             label='Расходы',
#         )
#         plt.xlabel('Месяц года')
#         plt.ylabel('Расход, в $.')
#         plt.title('Расходы по месяцам')
#         plt.legend()
#     elif len(object_dictinaries) > 0 and len(expenses_object_dictinaries) == 0:
#         name_of_file = './media/grafics/' + str(chat.id) + 'incomes_by_' + group_by + '.png'
#         if os.path.exists(name_of_file):
#             os.remove(name_of_file)
#         dates = set(
#             i[group_by].strftime("%Y-%m")
#             for i in object_dictinaries
#         )
#         grouped = [
#             (date, [
#                 i[value_for_sum] for i in object_dictinaries
#                 if i[group_by].strftime("%Y-%m") == date
#             ]) for date in dates
#         ]
#         summed = [
#             {
#                 group_by: k,
#                 value_for_sum: sum(v)
#             } for k, v in grouped
#         ]
#         xs_dates = [obj[group_by] for obj in summed]
#         ys_values = [obj[value_for_sum] for obj in summed]
#         # столбчатый график
#         plt.bar(
#             xs_dates,
#             ys_values,
#             label='Доходы',
#         )
#         plt.xlabel('Месяц года')
#         plt.ylabel('Доход, в $.')
#         plt.title('Доходы по месяцам')
#         plt.legend()
#     elif len(object_dictinaries) > 0 and len(expenses_object_dictinaries) > 0:
#         name_of_file = './media/grafics/' + str(chat.id) + 'incomes_and_expenses_by_' + group_by + '.png'
#         if os.path.exists(name_of_file):
#             os.remove(name_of_file)
#         # получить даты из доходов
#         incomes_dates = [i[group_by] for i in object_dictinaries]
#         # получить даты из расходов
#         expenses_dates = [i[group_by] for i in expenses_object_dictinaries]
#         # объединить списки
#         incomes_dates.extend(expenses_dates)
#         # отсортировать списки
#         incomes_dates.sort()
#         # преобразовать элементы в строку
#         # превратить в множество
#         dates = set([i.strftime("%Y-%m") for i in incomes_dates])
#         grouped = [
#             (date, [
#                 i[value_for_sum] for i in object_dictinaries
#                 if i[group_by].strftime("%Y-%m") == date
#             ]) for date in dates
#         ]
#         grouped_expenses = [
#             (date, [
#                 i[value_for_sum] for i in expenses_object_dictinaries
#                 if i[group_by].strftime("%Y-%m") == date
#             ]) for date in dates
#         ]

#         summed = [
#             {
#                 group_by: k,
#                 value_for_sum: sum(v)
#             } for k, v in grouped
#         ]
#         xs_dates = [obj[group_by] for obj in summed]
#         ys_values = [obj[value_for_sum] for obj in summed]
#         expenses_summed = [
#             {
#                 group_by: k,
#                 value_for_sum: sum(v)
#             } for k, v in grouped_expenses
#         ]
#         ys_expenses_values = [obj[value_for_sum] for obj in expenses_summed]
#         x = np.arange(len(xs_dates))  # the label locations
#         width = 0.35  # the width of the bars

#         fig, ax = plt.subplots()
#         rects1 = ax.bar(x - width/2, ys_values, width, label='Доходы')
#         rects2 = ax.bar(x + width/2, ys_expenses_values, width, label='Расходы')

#         # Add some text for labels, title and custom x-axis tick labels, etc.
#         ax.set_ylabel('Сумма')
#         ax.set_title('Доходы и расходы')
#         ax.set_xticks(x, xs_dates)
#         ax.legend()

#         ax.bar_label(rects1, padding=3)
#         ax.bar_label(rects2, padding=3)

#         fig.tight_layout()

#     plt.savefig(name_of_file)
#     file_with_grofics = open(name_of_file, 'rb')
#     plt.close()
#     return file_with_grofics