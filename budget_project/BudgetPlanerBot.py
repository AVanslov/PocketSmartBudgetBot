"""
Функции для работы телеграм бота. 
На время работы над основным кодом сервиса выключены.
"""

# # Budget_v1
# import django
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# import re

# matplotlib.use('Agg')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_project.settings')
# django.setup()


# from telegram.ext import (
#     CallbackQueryHandler,
#     CommandHandler,
#     Filters,
#     MessageHandler,
#     Updater,
# )
# from telegram import (
#     # ReplyKeyboardRemove,
#     # ReplyKeyboardMarkup,
#     Bot,
#     InlineKeyboardButton,
#     InlineKeyboardMarkup,
#     ReplyKeyboardRemove,
# )

# from bot import views
# import categoriesupdate
# import telegramcalendar
# import messages
# import utils


# chat_id = 6284162894

# bot = Bot(token='7020824901:AAFw9qE5wBw-btZmWChKHU9k5jygjpZ49Ww')

# updater = Updater(token='7020824901:AAFw9qE5wBw-btZmWChKHU9k5jygjpZ49Ww')

# MESSAGES_ID = []


# def auto_delete_previouse_message(update, context):
#     # if update.callback_query is None:
#     #     current_message_number = update.message.message_id
#     # else:
#     #     current_message_number = update.callback_query.message.message_id
#     # if MESSAGES_ID:
#     #     context.bot.delete_message(
#     #         chat_id=update.effective_chat.id,
#     #         message_id=MESSAGES_ID[len(MESSAGES_ID) - 1]
#     #     )
#     #     MESSAGES_ID.clear()
#     # MESSAGES_ID.append(current_message_number)
#     pass


# def error_empty_ection(update, context):
#     chat = update.effective_chat
#     message = 'Пожалуйста, сначала нажмите на кнопку, чтобы выбрать действие'
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Спланировать бюджет', callback_data='ignore'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Добавить доходы', callback_data='add_incomes'
#             ),
#             InlineKeyboardButton(
#                 'Добавить расходы', callback_data='add_expenses'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Редактировать категории доходов', callback_data='incomes_category_update'
#             ),
#             InlineKeyboardButton(
#                 'Редактировать категории расходов', callback_data='expenses_category_update'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Показать отчет за год', callback_data='result'
#             ),
#             InlineKeyboardButton(
#                 'Показать отчет за месяц', callback_data='ignore'
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     auto_delete_previouse_message(update, context)

#     context.bot.send_message(
#         chat_id=chat.id,
#         text=message,
#         reply_markup=reply_markup,
#     )


# def say_hi(update, context):
#     chat = update.effective_chat
#     name = update.message.chat.first_name
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Спланировать бюджет', callback_data='ignore'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Добавить доходы', callback_data='add_incomes'
#             ),
#             InlineKeyboardButton(
#                 'Добавить расходы', callback_data='add_expenses'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Редактировать категории доходов', callback_data='incomes_category_update'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Редактировать каткгории расходов', callback_data='expenses_category_update'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Показать отчет за год', callback_data='result'
#             ),
#             InlineKeyboardButton(
#                 'Показать отчет за месяц', callback_data='ignore'
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     message = (
#         '''
# <b>Приветствем, {}!</b>\n
# <b>SimBu</b> - Simple Budget - это сервис для ведения бюджета, где вы сможете:\n
# ✅ Записывать свои расходы и доходы\n
# ✅ Получать подробный отчет за текущий год в виде графика.\n
# <b>Автор:</b> <i>Бучельников Александр </i>
# <b>Текущая версия</b> <i>0.0.5 от 15.04.2024</i>\n
# Добавлена возможность удалять категории расходов.
# ''').format(name)

#     auto_delete_previouse_message(update, context)

#     context.bot.send_message(
#         chat_id=chat.id,
#         text=message,
#         parse_mode='HTML',
#         reply_markup=reply_markup,
#     )


# INCOME = []
# EXPENSE = []

# LAST_ACTIONS = []
# CHOSEN_CATEGORY = []


# def add_incomes(update, context):
#     chat = update.effective_chat
#     views.get_or_create_user(chat)
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Прекратить ввод данных и начать сначала',
#                 callback_data='stop_add_data',
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     auto_delete_previouse_message(update, context)

#     context.bot.send_message(
#         chat_id=chat.id,
#         text='Введите комментарий',
#         reply_markup=reply_markup
#     )
#     LAST_ACTIONS.append('income')


# def add_expenses(update, context):
#     chat = update.effective_chat
#     views.get_or_create_user(chat)
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Прекратить ввод данных и начать сначала',
#                 callback_data='stop_add_data',
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     auto_delete_previouse_message(update, context)

#     context.bot.send_message(
#         chat_id=chat.id,
#         text='Введите комментарий',
#         reply_markup=reply_markup
#     )
#     LAST_ACTIONS.append('expense')


# def add_name(update, context):
#     # получить из поля текст значение и записать его в список INCOME
#     # показать выбор категории
#     chat = update.effective_chat
#     value = update.message.text
#     if not value:
#         value = None
#     # добавляем валидацию
#     # значение должно состоять только из букв
#     # если не буквы и не пусто - заново отправляется сообщение введите комментарий
#     # если путо, ставим None
#     if LAST_ACTIONS[-1] == 'income':
#         INCOME.append(value)
#         keyboard = categoriesupdate.inline_categories_buttons(
#             type='incomes',
#             author=chat
#         )
#     else:
#         EXPENSE.append(value)
#         keyboard = categoriesupdate.inline_categories_buttons(
#             type='expenses',
#             author=chat
#         )

#     default_buttons = [
#         InlineKeyboardButton(
#             'Редактировать категории',
#             callback_data='incomes_category_update'
#         ),
#         InlineKeyboardButton(
#             'Прекратить ввод данных и начать сначала',
#             callback_data='stop_add_data',
#         ),
#     ]

#     for i in default_buttons:
#         a = []
#         a.append(i)
#         keyboard.append(a)
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     auto_delete_previouse_message(update, context)

#     context.bot.send_message(
#         chat_id=chat.id,
#         text='Выберите категорию',
#         reply_markup=reply_markup,
#     )


# def add_value_message(update, context):
#     """
#     Принимает значение суммы и отправляет сообщение
#     с предложением завершить процесс добавления данных.
#     """

#     chat = update.effective_chat
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Прекратить ввод данных и начать сначала',
#                 callback_data='stop_add_data',
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     auto_delete_previouse_message(update, context)

#     context.bot.send_message(
#         chat_id=chat.id,
#         text='Введите сумму',
#         reply_markup=reply_markup,

#     )


# def add_value(update, context):
#     value = update.message.text
#     if LAST_ACTIONS[-1] == 'income':
#         INCOME.append(value)

#     else:
#         EXPENSE.append(value)

#     auto_delete_previouse_message(update, context)

#     calendar_handler(update, context)


# def calendar_handler(update, context):

#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text='Выберите дату',
#         reply_markup=telegramcalendar.create_calendar()
#     )


# def inline_handler(update, context):
#     query = update.callback_query
#     (kind, _, _, _, _) = utils.separate_callback_data(query.data)
#     if kind == messages.CALENDAR_CALLBACK:
#         inline_calendar_handler(update, context)
#     else:
#         print('Something wrong')


# def inline_calendar_handler(update, context):
#     selected, date = telegramcalendar.process_calendar_selection(update, context)
#     chat = update.effective_chat
#     if selected:
#         print(date)
#         if LAST_ACTIONS[-1] == 'income':
#             INCOME.append(date)

#             comment, category, value, date = tuple(INCOME)
#             # chat = update.effective_chat
#             views.save_income_in_db(str(comment), category, value, date, author=chat)
#             INCOME.clear()
#             context.bot.send_message(
#                 chat_id=update.callback_query.from_user.id,
#                 text=messages.calendar_response_message % (date.strftime("%d/%m/%Y")),
#                 reply_markup=ReplyKeyboardRemove()
#             )
#         else:
#             EXPENSE.append(date)
#             comment, category, value, date = tuple(EXPENSE)
#             # chat = update.effective_chat
#             views.save_expense_in_db(str(comment), category, value, date, author=chat)
#             EXPENSE.clear()
#             LAST_ACTIONS.clear()
#             context.bot.send_message(
#                 chat_id=update.callback_query.from_user.id,
#                 text=messages.calendar_response_message % (date.strftime("%d/%m/%Y")),
#                 reply_markup=ReplyKeyboardRemove()
#             )

#         keyboard = [
#             [
#                 InlineKeyboardButton(
#                     'Добавить доходы', callback_data='add_incomes'
#                 ),
#                 InlineKeyboardButton(
#                     'Добавить расходы', callback_data='add_expenses'
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     'Редактировать категории доходов', callback_data='incomes_category_update'
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     'Редактировать категории расходов', callback_data='expenses_category_update'
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     'Показать отчет за год', callback_data='result'
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     'Удалить все доходы', callback_data='delete_all'
#                 ),
#                 InlineKeyboardButton(
#                     'Удалить все расходы', callback_data='delete_all_expenses'
#                 ),
#             ],
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)

#         context.bot.send_message(
#             chat_id=chat.id,
#             text='Показать результат?',
#             reply_markup=reply_markup,
#         )


# def delete_all(update, context):
#     chat = update.effective_chat
#     views.delete_all(chat)
#     INCOME.clear()
#     EXPENSE.clear()
#     LAST_ACTIONS.clear()
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Добавить доходы', callback_data='add_incomes'
#             ),
#             InlineKeyboardButton(
#                 'Добавить расходы', callback_data='add_expenses'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Показать отчет за год', callback_data='result'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Удалить все доходы', callback_data='delete_all'
#             ),
#             InlineKeyboardButton(
#                 'Удалить все расходы', callback_data='delete_all_expenses'
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     auto_delete_previouse_message(update, context)

#     context.bot.send_message(
#         chat_id=chat.id,
#         text='Показать результат?',
#         reply_markup=reply_markup,
#     )


# def delete_all_expenses(update, context):
#     chat = update.effective_chat
#     views.delete_all_expenses(chat)
#     INCOME.clear()
#     EXPENSE.clear()
#     LAST_ACTIONS.clear()
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Добавить доходы', callback_data='add_incomes'
#             ),
#             InlineKeyboardButton(
#                 'Добавить расходы', callback_data='add_expenses'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Показать отчет за год', callback_data='result'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Удалить все доходы', callback_data='delete_all'
#             ),
#             InlineKeyboardButton(
#                 'Удалить все расходы', callback_data='delete_all_expenses'
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     auto_delete_previouse_message(update, context)

#     context.bot.send_message(
#         chat_id=chat.id,
#         text='Показать результат?',
#         reply_markup=reply_markup,
#     )


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


# def create_monthly_report_message(chat):
#     object_dictinaries = views.get_report(chat)

#     if len(object_dictinaries) == 0:
#         return 'Список расходов пуст'

#     ints = []
#     for i in object_dictinaries:
#         ints.append(i['value'])

#     # переменные для графика с яблоками
#     # max_value = max(ints)
#     # max_leight = 12

#     massage = ''
#     for i in object_dictinaries:
#         massage += str(i['date']) + ' '
#         massage += str(i['comment']) + ' '
#         massage += str(i['category']) + ' '
#         massage += str(i['value']) + ' '
#         # massage += str(i.author)
#         massage += '\n'

#         # создание схематичного отображения расхода в виде яблок
#         # (график в виде яблок)
#         # for a in list(range(0, round(i['value']*max_leight/max_value))):
#         #     massage += '🍏'
#         # massage += '\n'

#     return massage


# def send_message_with_result(update, context):
#     chat = update.effective_chat
#     chat_id = chat.id
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Добавить доходы', callback_data='add_incomes'
#             ),
#             InlineKeyboardButton(
#                 'Добавить расходы', callback_data='add_expenses'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Показать отчет за год', callback_data='result'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Удалить все доходы', callback_data='delete_all'
#             ),
#             InlineKeyboardButton(
#                 'Удалить все расходы', callback_data='delete_all_expenses'
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     auto_delete_previouse_message(update, context)
#     context.bot.send_photo(
#         chat_id,
#         create_grafic(chat, group_by='date', value_for_sum='value', type='fig'),
#         reply_markup=reply_markup,
#     )


# def stop_add_data(update, context):
#     chat = update.effective_chat
#     INCOME.clear()
#     EXPENSE.clear()
#     LAST_ACTIONS.clear()
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Добавить доходы', callback_data='add_incomes'
#             ),
#             InlineKeyboardButton(
#                 'Добавить расходы', callback_data='add_expenses'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Редактировать категории доходов', callback_data='incomes_category_update'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Редактировать категории расходов', callback_data='expenses_category_update'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Показать отчет за год', callback_data='result'
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     auto_delete_previouse_message(update, context)
#     context.bot.send_message(
#         chat_id=chat.id,
#         text=(
#             'Вы можете начать сначала.'
#         ),
#         reply_markup=reply_markup,
#     )


# def add_new_category_message(update, context):
#     chat = update.effective_chat
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Прекратить ввод данных и начать сначала',
#                 callback_data='stop_add_data',
#             ),
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     auto_delete_previouse_message(update, context)
#     context.bot.send_message(
#         chat_id=chat.id,
#         text='Введите название категории',
#         reply_markup=reply_markup,

#     )


# def add_new_category(update, context):
#     chat = update.effective_chat
#     value = update.message.text
#     if LAST_ACTIONS[-1] == 'incomes_category_update':
#         views.create_income_category(value, author=chat)
#         categoriesupdate.incomes_category_update(update, context)
#     elif LAST_ACTIONS[-1] == 'expense_category_update':
#         views.create_expense_category(value, author=chat)
#         categoriesupdate.expenses_category_update(update, context)
#     auto_delete_previouse_message(update, context)


# def validate_data(update, context):
#     chat = update.effective_chat
#     value = update.message.text
#     # добавляем валидацию
#     # значение должно состоять только из букв
#     # если не буквы и не пусто - заново отправляется сообщение введите комментарий
#     # если путо, ставим None
#     if not LAST_ACTIONS:
#         error_empty_ection(update, context)
#     else:
#         if LAST_ACTIONS[-1] == 'income':
#             if (re.fullmatch(r'^\D+$', value) or not value) and not INCOME:
#                 add_name(update, context)

#             elif not re.fullmatch(r'^\D+$', value) and not INCOME:
#                 context.bot.send_message(
#                     chat_id=chat.id,
#                     text='Ай-йай-йай, в комментарии должна быть хотя бы одна буква',
#                 )
#                 add_incomes(update, context)

#             elif re.fullmatch(r'^\d+$', value) and INCOME:
#                 add_value(update, context)

#             elif not re.fullmatch(r'^\d+$', value) and INCOME:
#                 context.bot.send_photo(
#                     chat.id,
#                     open(
#                         './media/'
#                         'error_image_value_expect_numbers.png',
#                         'rb'
#                     ),
#                 )
#                 context.bot.send_message(
#                     chat_id=chat.id,
#                     text='В cумме должны быть только цифры',
#                 )
#                 add_value_message(update, context)

#         elif LAST_ACTIONS[-1] == 'expense':
#             if (re.search(r'^\D+$', value) or not value) and not EXPENSE:
#                 add_name(update, context)

#             elif not re.search(r'^\D+$', value) and not EXPENSE:
#                 context.bot.send_message(
#                     chat_id=chat.id,
#                     text='Ай-йай-йай, в комментарии должна быть хотя бы одна буква',
#                 )
#                 add_expenses(update, context)

#             elif re.fullmatch(r'^\d+$', value) and EXPENSE:
#                 add_value(update, context)

#             elif not re.fullmatch(r'^\d+$', value) and EXPENSE:
#                 context.bot.send_photo(
#                     chat.id,
#                     open(
#                         './media/'
#                         'error_image_value_expect_numbers.png',
#                         'rb'
#                     ),
#                 )
#                 context.bot.send_message(
#                     chat_id=chat.id,
#                     text='В cумме должны быть только цифры',
#                 )
#                 add_value_message(update, context)
#         elif LAST_ACTIONS[-1] == 'incomes_category_update':
#             if (re.search(r'^\D+$', value) or not value):
#                 add_new_category(update, context)
#             elif not re.search(r'^\D+$', value):
#                 context.bot.send_message(
#                     chat_id=chat.id,
#                     text='Ай-йай-йай, в названии категории должна быть хотя бы одна буква',
#                 )
#                 add_new_category_message(update, context)
#         else:
#             error_empty_ection(update, context)


# def inline_button_handler(update, context):
#     query = update.callback_query
#     variant = query.data
#     query.answer()
#     print(variant)
#     if variant == 'add_incomes':
#         if INCOME:
#             INCOME.clear()
#             EXPENSE.clear()
#             LAST_ACTIONS.clear()
#         add_incomes(update, context)
#     elif variant == 'add_expenses':
#         if EXPENSE:
#             INCOME.clear()
#             EXPENSE.clear()
#             LAST_ACTIONS.clear()
#         add_expenses(update, context)
#     elif variant == 'delete_category':
#         if CHOSEN_CATEGORY[-1] in categoriesupdate.list_of_author_categories(
#             type='incomes',
#             author=update.effective_chat
#         ):
#             views.delete_category(
#                 type='incomes',
#                 category=CHOSEN_CATEGORY[-1],
#                 author=update.effective_chat
#             )

#         elif CHOSEN_CATEGORY[-1] in categoriesupdate.list_of_author_categories(
#             type='expenses',
#             author=update.effective_chat
#         ):
#             views.delete_category(
#                 type='expenses',
#                 category=CHOSEN_CATEGORY[-1],
#                 author=update.effective_chat
#             )
#         categoriesupdate.incomes_category_update(update, context)
#     elif variant in categoriesupdate.list_of_author_categories(
#         type='incomes',
#         author=update.effective_chat
#     ) and LAST_ACTIONS[-1] == 'incomes_category_update':
#         CHOSEN_CATEGORY.append(variant)
#         categoriesupdate.income_category_update(update, context)
#     elif variant in categoriesupdate.list_of_author_categories(
#         type='incomes', author=update.effective_chat
#     ):
#         INCOME.append(views.get_category_object(type='incomes', category=variant, author=update.effective_chat)) # нужно записать id объекта, у которого вариант и автор совпадают
#         add_value_message(update, context)
#     elif variant in categoriesupdate.list_of_author_categories(
#         type='expenses', author=update.effective_chat
#     ):
#         print(variant)
#         EXPENSE.append(views.get_category_object(type='expenses', category=variant, author=update.effective_chat)) # нужно записать id объекта, у которого вариант и автор совпадают
#         add_value_message(update, context)
#     elif variant == 'result':
#         send_message_with_result(update, context)
#     elif variant == 'delete_all':
#         delete_all(update, context)
#     elif variant == 'delete_all_expenses':
#         delete_all_expenses(update, context)
#     elif variant == 'stop_add_data':
#         stop_add_data(update, context)
#     elif variant == 'incomes_category_update':
#         LAST_ACTIONS.append('incomes_category_update')
#         categoriesupdate.incomes_category_update(update, context)
#     elif variant == 'add_new_category':
#         add_new_category_message(update, context)
#     else:
#         inline_handler(update, context)


# updater.dispatcher.add_handler(
#     CommandHandler('start', say_hi)
# )
# updater.dispatcher.add_handler(
#     CallbackQueryHandler(inline_button_handler)
# )
# updater.dispatcher.add_handler(
#     MessageHandler(Filters.text, validate_data)
# )


# updater.start_polling()
# updater.idle()
