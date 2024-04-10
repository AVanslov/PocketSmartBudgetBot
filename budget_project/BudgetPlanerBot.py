# Budget_v1
import django
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
matplotlib.use('Agg')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_project.settings')
django.setup()


from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)
from telegram import (
    # ReplyKeyboardRemove,
    # ReplyKeyboardMarkup,
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import views


chat_id = 6284162894

bot = Bot(token='7020824901:AAFw9qE5wBw-btZmWChKHU9k5jygjpZ49Ww')

updater = Updater(token='7020824901:AAFw9qE5wBw-btZmWChKHU9k5jygjpZ49Ww')

INCOMES_CATEGORIES_LIST = [
    'category_salary',
    'category_obligation',
    'category_stocks',
    'category_investments',
    'category_freelance',
    'category_business',
]

EXPENSES_CATEGORIES_LIST = [
    'category_products',
    'category_rent',
    'category_flowers',
    'category_clothes',
    'category_pets',
    'category_trips',
]


def say_hi(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    keyboard = [
        [
            InlineKeyboardButton(
                'Добавить доходы', callback_data='add_incomes'
            ),
            InlineKeyboardButton(
                'Добавить расходы', callback_data='add_expenses'
            ),
        ],
        [
            InlineKeyboardButton(
                'Показать отчет за год', callback_data='result'
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = (
        '''
<b>Приветствем, {}!</b>\n
<b>SimBu</b> - Simple Budget - это сервис для ведения бюджета, где вы сможете:\n
✅ Записывать свои расходы и доходы\n
✅ Настраивать категории расходов и доходов\n
✅ Получать подробный отчет за текущий год в виде графика и диаграммы.\n
<b>Текущая версия</b> <i>0.0.1 от 10.04.2024</i>\n
<b>Автор:</b> <i>Бучельников Александр </i>
''').format(name)
    context.bot.send_message(
        chat_id=chat.id,
        text=message,
        parse_mode='HTML',
        reply_markup=reply_markup,
    )


INCOME = []
EXPENSE = []

LAST_ACTIONS = []


def add_incomes(update, context):
    chat = update.effective_chat
    views.get_or_create_user(chat)
    context.bot.send_message(
        chat_id=chat.id,
        text='Введите комментарий',
    )
    LAST_ACTIONS.append('income')


def add_expenses(update, context):
    chat = update.effective_chat
    views.get_or_create_user(chat)
    context.bot.send_message(
        chat_id=chat.id,
        text='Введите комментарий',
    )
    LAST_ACTIONS.append('expense')


def add_name(update, context):
    # получить из поля текст значение и записать его в список INCOME
    # показать выбор категории
    chat = update.effective_chat
    value = update.message.text
    if LAST_ACTIONS[-1] == 'income':
        INCOME.append(value)
        keyboard = [
            [
                InlineKeyboardButton(
                    'Зарплата', callback_data='category_salary'
                ),
                InlineKeyboardButton(
                    'Облигации', callback_data='category_obligation'
                ),
            ],
            [
                InlineKeyboardButton(
                    'Акции', callback_data='category_stocks'
                ),
                InlineKeyboardButton(
                    'Инвестиции', callback_data='category_investments'
                ),
            ],
            [
                InlineKeyboardButton(
                    'Фриланс', callback_data='category_freelance'
                ),
                InlineKeyboardButton(
                    'Бизнес', callback_data='category_business'
                ),
            ],
            [
                InlineKeyboardButton(
                    'delete', callback_data='delete_all'
                ),
            ],
        ]
    else:
        EXPENSE.append(value)
        keyboard = [
            [
                InlineKeyboardButton(
                    'Продукты', callback_data='category_products'
                ),
                InlineKeyboardButton(
                    'Аренда', callback_data='category_rent'
                ),
            ],
            [
                InlineKeyboardButton(
                    'Цветы', callback_data='category_flowers'
                ),
                InlineKeyboardButton(
                    'Одежда', callback_data='category_clothes'
                ),
            ],
            [
                InlineKeyboardButton(
                    'Питомцы', callback_data='category_pets'
                ),
                InlineKeyboardButton(
                    'Путешествия', callback_data='category_trips'
                ),
            ],
            [
                InlineKeyboardButton(
                    'delete', callback_data='delete_all_expenses'
                ),
            ],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat.id,
        text='Выберите категорию',
        reply_markup=reply_markup,
    )


def add_value_message(update, context):
    # добавить валидацию должны быть буквы
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Введите сумму',
    )


def add_value(update, context):
    value = update.message.text
    if LAST_ACTIONS[-1] == 'income':
        INCOME.append(value)

        # указать date (date)
        # отправить запрос на запись данных в базу данных
        # добавить проверку на колличество экземпляров
        # если неправильное число, очистить кортеж
        # и отправить пользователя заново заполнять имя
        comment, category, value = tuple(INCOME)
        chat = update.effective_chat
        views.save_income_in_db(str(comment), str(category), str(value), author=chat)
        INCOME.clear()
    else:
        EXPENSE.append(value)
        comment, category, value = tuple(EXPENSE)
        chat = update.effective_chat
        views.save_expense_in_db(str(comment), str(category), str(value), author=chat)
        EXPENSE.clear()
        LAST_ACTIONS.clear()
    keyboard = [
        [
            InlineKeyboardButton(
                'Добавить доходы', callback_data='add_incomes'
            ),
            InlineKeyboardButton(
                'Добавить расходы', callback_data='add_expenses'
            ),
        ],
        [
            InlineKeyboardButton(
                'Показать отчет за год', callback_data='result'
            ),
        ],
        [
            InlineKeyboardButton(
                'Удалить все доходы', callback_data='delete_all'
            ),
            InlineKeyboardButton(
                'Удалить все расходы', callback_data='delete_all_expenses'
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat.id,
        text='Показать результат?',
        reply_markup=reply_markup,
    )


def add_date(update, context):
    # вызвать функцию, создающую календарь
    # принять данные из inline keybord
    # преобразовать полученные данные в объект datetime
    # добавить значение в tuple
    # распаковать tuple
    # вызвать функцию для добавления записи в БД
    # очистить tuple
    # очистить список с командами
    pass


def delete_all(update, context):
    chat = update.effective_chat
    views.delete_all(chat)
    keyboard = [
        [
            InlineKeyboardButton(
                'Добавить доходы', callback_data='add_incomes'
            ),
            InlineKeyboardButton(
                'Добавить расходы', callback_data='add_expenses'
            ),
        ],
        [
            InlineKeyboardButton(
                'Показать отчет за год', callback_data='result'
            ),
        ],
        [
            InlineKeyboardButton(
                'Удалить все доходы', callback_data='delete_all'
            ),
            InlineKeyboardButton(
                'Удалить все расходы', callback_data='delete_all_expenses'
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat.id,
        text='Показать результат?',
        reply_markup=reply_markup,
    )


def delete_all_expenses(update, context):
    chat = update.effective_chat
    views.delete_all_expenses(chat)
    keyboard = [
        [
            InlineKeyboardButton(
                'Добавить доходы', callback_data='add_incomes'
            ),
            InlineKeyboardButton(
                'Добавить расходы', callback_data='add_expenses'
            ),
        ],
        [
            InlineKeyboardButton(
                'Показать отчет за год', callback_data='result'
            ),
        ],
        [
            InlineKeyboardButton(
                'Удалить все доходы', callback_data='delete_all'
            ),
            InlineKeyboardButton(
                'Удалить все расходы', callback_data='delete_all_expenses'
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat.id,
        text='Показать результат?',
        reply_markup=reply_markup,
    )


def create_grafic(chat, group_by: str, value_for_sum: str, type: str = 'bar'):
    """
    Создает график на основе списка словарей
    - каждый словарь
    - объект таблицы Income
    - группирует значения value по датам
    - возвращает закодированное в base 64 изображение графика.
    """
    # получаем [{'value':5000},{}]
    # перебираем и из каждого словаря достаем дату
    # из каждой даты достаем значение месяца и года
    # объявлем пустой список для dates
    # добавляем в него уникальные год - месяц - это горизонтальныя ось
    # объявляем пустой список для value
    # для каждого уникального год-месяц получить value соответствующего словаря
    # получить список словарей для каждого месяца
    # сложить все value месяца и добавить в список для value - это вертикальная ось
    expenses_object_dictinaries = views.get_report_expenses(chat)

    object_dictinaries = views.get_report(chat)
    if len(object_dictinaries) == 0 and len(expenses_object_dictinaries) == 0:
        name_of_file = './media/add_some_data.png'
        file_without_grofics = open(name_of_file, 'rb')
        return file_without_grofics
    elif len(object_dictinaries) == 0 and len(expenses_object_dictinaries) > 0:
        name_of_file = './media/grafics/' + str(chat.id) + 'expenses_by_' + group_by + '.png'
        if os.path.exists(name_of_file):
            os.remove(name_of_file)
        dates = set(
                i[group_by].strftime("%Y-%m")
                for i in expenses_object_dictinaries
            )
        grouped_expenses = [
            (date, [
                i[value_for_sum] for i in expenses_object_dictinaries
                if i[group_by].strftime("%Y-%m") == date
            ]) for date in dates
        ]
        summed_expenses = [
            {
                group_by: k,
                value_for_sum: sum(v)
            } for k, v in grouped_expenses
        ]
        xs_dates = [obj[group_by] for obj in summed_expenses]
        ys_values = [obj[value_for_sum] for obj in summed_expenses]
        # столбчатый график
        plt.bar(
            xs_dates,
            ys_values,
            label='Расходы',
        )
        plt.xlabel('Месяц года')
        plt.ylabel('Расход, в $.')
        plt.title('Расходы по месяцам')
        plt.legend()
    elif len(object_dictinaries) > 0 and len(expenses_object_dictinaries) == 0:
        name_of_file = './media/grafics/' + str(chat.id) + 'incomes_by_' + group_by + '.png'
        if os.path.exists(name_of_file):
            os.remove(name_of_file)
        dates = set(
            i[group_by].strftime("%Y-%m")
            for i in object_dictinaries
        )
        grouped = [
            (date, [
                i[value_for_sum] for i in object_dictinaries
                if i[group_by].strftime("%Y-%m") == date
            ]) for date in dates
        ]
        summed = [
            {
                group_by: k,
                value_for_sum: sum(v)
            } for k, v in grouped
        ]
        xs_dates = [obj[group_by] for obj in summed]
        ys_values = [obj[value_for_sum] for obj in summed]
        # столбчатый график
        plt.bar(
            xs_dates,
            ys_values,
            label='Доходы',
        )
        plt.xlabel('Месяц года')
        plt.ylabel('Доход, в $.')
        plt.title('Доходы по месяцам')
        plt.legend()
    elif len(object_dictinaries) > 0 and len(expenses_object_dictinaries) > 0:
        name_of_file = './media/grafics/' + str(chat.id) + 'incomes_and_expenses_by_' + group_by + '.png'
        if os.path.exists(name_of_file):
            os.remove(name_of_file)
        # получить даты из доходов
        incomes_dates = [i[group_by] for i in object_dictinaries]
        # получить даты из расходов
        expenses_dates = [i[group_by] for i in expenses_object_dictinaries]
        # объединить списки
        incomes_dates.extend(expenses_dates)
        # отсортировать списки
        incomes_dates.sort()
        # преобразовать элементы в строку
        # превратить в множество
        dates = set([i.strftime("%Y-%m") for i in incomes_dates])
        grouped = [
            (date, [
                i[value_for_sum] for i in object_dictinaries
                if i[group_by].strftime("%Y-%m") == date
            ]) for date in dates
        ]
        grouped_expenses = [
            (date, [
                i[value_for_sum] for i in expenses_object_dictinaries
                if i[group_by].strftime("%Y-%m") == date
            ]) for date in dates
        ]

        summed = [
            {
                group_by: k,
                value_for_sum: sum(v)
            } for k, v in grouped
        ]
        xs_dates = [obj[group_by] for obj in summed]
        ys_values = [obj[value_for_sum] for obj in summed]
        expenses_summed = [
            {
                group_by: k,
                value_for_sum: sum(v)
            } for k, v in grouped_expenses
        ]
        ys_expenses_values = [obj[value_for_sum] for obj in expenses_summed]
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

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()

    plt.savefig(name_of_file)
    file_with_grofics = open(name_of_file, 'rb')
    plt.close()
    return file_with_grofics


def create_monthly_report_message(chat):
    object_dictinaries = views.get_report(chat)

    if len(object_dictinaries) == 0:
        return 'Список расходов пуст'

    ints = []
    for i in object_dictinaries:
        ints.append(i['value'])

    # переменные для графика с яблоками
    # max_value = max(ints)
    # max_leight = 12

    massage = ''
    for i in object_dictinaries:
        massage += str(i['date']) + ' '
        massage += str(i['comment']) + ' '
        massage += str(i['category']) + ' '
        massage += str(i['value']) + ' '
        # massage += str(i.author)
        massage += '\n'

        # создание схематичного отображения расхода в виде яблок
        # (график в виде яблок)
        # for a in list(range(0, round(i['value']*max_leight/max_value))):
        #     massage += '🍏'
        # massage += '\n'

    return massage


def send_message_with_result(update, context):
    chat = update.effective_chat
    keyboard = [
        [
            InlineKeyboardButton(
                'Добавить доходы', callback_data='add_incomes'
            ),
            InlineKeyboardButton(
                'Добавить расходы', callback_data='add_expenses'
            ),
        ],
        [
            InlineKeyboardButton(
                'Показать отчет за год', callback_data='result'
            ),
        ],
        [
            InlineKeyboardButton(
                'Удалить все доходы', callback_data='delete_all'
            ),
            InlineKeyboardButton(
                'Удалить все расходы', callback_data='delete_all_expenses'
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_photo(
        chat_id,
        create_grafic(chat, group_by='date', value_for_sum='value', type='fig'),
        reply_markup=reply_markup,
    )


def inline_button_handler(update, context):
    query = update.callback_query
    variant = query.data
    query.answer()
    print(variant)
    if variant == 'add_incomes':
        add_incomes(update, context)
    elif variant == 'add_expenses':
        add_expenses(update, context)
    elif variant in INCOMES_CATEGORIES_LIST:
        INCOME.append(variant)
        add_value_message(update, context)
    elif variant in EXPENSES_CATEGORIES_LIST:
        print(variant)
        EXPENSE.append(variant)
        add_value_message(update, context)
    elif variant == 'result':
        send_message_with_result(update, context)
    elif variant == 'delete_all':
        delete_all(update, context)
    elif variant == 'delete_all_expenses':
        delete_all_expenses(update, context)


updater.dispatcher.add_handler(
    CommandHandler('start', say_hi)
)
updater.dispatcher.add_handler(
    CallbackQueryHandler(inline_button_handler)
)
updater.dispatcher.add_handler(
    MessageHandler(Filters.regex(r'^\d+$'), add_value)
)
updater.dispatcher.add_handler(
    MessageHandler(Filters.text, add_name)
)


updater.start_polling()
updater.idle()
