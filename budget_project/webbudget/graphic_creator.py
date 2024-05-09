from django.conf import settings
import matplotlib
import matplotlib.pyplot as plt
from bot.models import Money
import numpy as np

def incomes_or_expenses_grafic(incomes_object_dictinaries, name_of_file):
    dates = set(
            i['date'].strftime("%Y-%m")
            for i in incomes_object_dictinaries
        )
    grouped_expenses = [
        (date, [
            i['value'] for i in incomes_object_dictinaries
            if i['date'].strftime("%Y-%m") == date
        ]) for date in dates
    ]
    summed_expenses = [
        {
            'date': k,
            'value': sum(v)
        } for k, v in grouped_expenses
    ]
    xs_dates = [obj['date'] for obj in summed_expenses]
    ys_values = [obj['value'] for obj in summed_expenses]
    # столбчатый график
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Tahoma', 'DejaVu Sans',
                            'Lucida Grande', 'Verdana']
    plt.figure(facecolor='#f2f2f2', figsize=(5, 2.7))
    plt.axes().set_facecolor('#f2f2f2')
    plt.bar(
        xs_dates,
        ys_values,
        label='Incomes',
        color='#CEE741',
    )
    plt.xlabel('Month')
    plt.ylabel('Income, in $.')
    plt.title('Incomes by months')
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # plt.legend()

    plt.savefig(name_of_file)
    file_with_grafics = open(name_of_file, 'rb')
    plt.close()
    return file_with_grafics


def incomes_and_expenses_grafic(incomes_object_dictinaries, expenses_object_dictinaries, name_of_file):
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
            i['value'] for i in incomes_object_dictinaries
            if i['date'].strftime("%Y-%m") == date
        ]) for date in dates
    ]
    grouped_expenses = [
        (date, [
            i['value'] for i in expenses_object_dictinaries
            if i['date'].strftime("%Y-%m") == date
        ]) for date in dates
    ]

    summed = [
        {
            'date': k,
            'value': sum(v)
        } for k, v in grouped
    ]
    xs_dates = [obj['date'] for obj in summed]
    ys_values = [obj['value'] for obj in summed]
    expenses_summed = [
        {
            'date': k,
            'value': sum(v)
        } for k, v in grouped_expenses
    ]
    ys_expenses_values = [obj['value'] for obj in expenses_summed]
    x = np.arange(len(xs_dates))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, ys_values, width, label='Доходы')
    rects2 = ax.bar(x + width/2, ys_expenses_values, width, label='Расходы')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    
    ax.set_ylabel('Сумма')
    ax.set_title('Доходы и расходы')
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

    incomes_object_dictinaries = [money for money in Money.objects.filter(type__name='incomes', author=request.user).values()]
    expenses_object_dictinaries = [money for money in Money.objects.filter(type__name='expenses', author=request.user).values()]
    name_of_file =  settings.MEDIA_ROOT / 'add_some_data.png'
    if incomes_object_dictinaries and not expenses_object_dictinaries:
        return incomes_or_expenses_grafic(incomes_object_dictinaries, name_of_file)
    if expenses_object_dictinaries and not incomes_object_dictinaries:
        return incomes_or_expenses_grafic(expenses_object_dictinaries, name_of_file)
    if incomes_object_dictinaries and expenses_object_dictinaries:
        return incomes_and_expenses_grafic(incomes_object_dictinaries, expenses_object_dictinaries, name_of_file)


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