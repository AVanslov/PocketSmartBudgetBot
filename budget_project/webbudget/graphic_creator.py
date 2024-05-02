from django.conf import settings
import matplotlib
import matplotlib.pyplot as plt
from bot.models import Money
import numpy as np

def create_grafic(request):
    """
    Создает графики на основе объекта запроса.
    """

    expenses_object_dictinaries = [money for money in Money.objects.filter(type__name='incomes', author=request.user).values()]
    name_of_file =  settings.MEDIA_ROOT / 'add_some_data.png'

    dates = set(
            i['date'].strftime("%Y-%m")
            for i in expenses_object_dictinaries
        )
    grouped_expenses = [
        (date, [
            i['value'] for i in expenses_object_dictinaries
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
    plt.figure(facecolor='#f2f2f2')
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
    plt.legend()


    plt.savefig(name_of_file)
    file_with_grafics = open(name_of_file, 'rb')
    plt.close()
    return file_with_grafics