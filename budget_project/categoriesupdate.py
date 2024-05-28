"""
Функции для работы телеграм бота. 
На время работы над основным кодом сервиса выключены.
"""

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# from bot import views


# ADDITIONAL_BUTTONS = [
#         InlineKeyboardButton(
#             'Создать новую',
#             callback_data='add_new_category'
#         ),
#         InlineKeyboardButton(
#             'Удалить все',
#             callback_data='delete_all_categories',
#         ),
#         InlineKeyboardButton(
#                 'Главное меню',
#                 callback_data='stop_add_data',
#             ),
#     ]


# def list_of_author_categories(type: str, author):
#     """
#     Принимает тип incomes/expenses
#     возвращает список с категориями данного типа.
#     """
#     categories = []
#     if type == 'incomes':
#         for i in views.get_income_categories(author):
#             categories.append(i['category'])
#     else:
#         for i in views.get_expense_categories(author):
#             categories.append(i['category'])
#     return categories


# def inline_categories_buttons(type: str, author):
#     """
#     Принимает объект chat для получения информации об авторе
#     и тип incomes/expenses
#     Возвращает список со списками,
#     [
#         [
#             InlineKeyboardButton(
#                 'Название категории',
#                 callback_data='type, ID категории',
#             ),
#         ],
#     ].
#     """
#     keyboard = []
#     if type == 'incomes':
#         for i in views.get_income_categories(author):
#             list = []
#             list.append(
#                     InlineKeyboardButton(
#                         i['category'],
#                         callback_data=i['category']
#                     )
#                 )
#             keyboard.append(list)
#     else:
#         for i in views.get_expense_categories(author):
#             list = []
#             list.append(
#                     InlineKeyboardButton(
#                         i['category'],
#                         callback_data=i['category']
#                     )
#                 )
#             keyboard.append(list)
#     print(views.get_income_categories(author))
#     print(keyboard)
#     return keyboard


# def incomes_category_update(update, context):
#     """
#     Выводит inline кнопки с категориями доходов
#     Также показывает кнопки создать категорию и удалить все категории
#     Показывает надпись
#     - чтобы отредактировать существующую категорию, нажмите на нее ниже.
#     После выбора категории в этой функции,
#     должен запускаться процесс редактирования категории.
#     """
#     chat = update.effective_chat
#     keyboard = inline_categories_buttons(type='incomes', author=chat) # функция, которая возвращает inline кнопки с категориями

#     for i in ADDITIONAL_BUTTONS:
#         a = []
#         a.append(i)
#         keyboard.append(a)

#     reply_markup = InlineKeyboardMarkup(keyboard)
#     context.bot.send_message(
#         chat_id=chat.id,
#         text=(
#             'Чтобы удалить или отредактировать категорию, выберите ее ниже.'
#             'Будьте аккуратны: при удалении категории удаляются все записи'
#             'о доходах/расходах в данной категории.'
#         ),
#         reply_markup=reply_markup,
#     )


# def expenses_category_update(update, context):
#     """
#     Выводит inline кнопки с категориями расходов
#     Также показывает кнопки создать категорию и удалить все категории
#     Показывает надпись
#     - чтобы отредактировать существующую категорию, нажмите на нее ниже.
#     После выбора категории в этой функции,
#     должен запускаться процесс редактирования категории.
#     """
#     chat = update.effective_chat
#     keyboard = inline_categories_buttons(type='expense', author=chat) # функция, которая возвращает inline кнопки с категориями

#     for i in ADDITIONAL_BUTTONS:
#         a = []
#         a.append(i)
#         keyboard.append(a)

#     reply_markup = InlineKeyboardMarkup(keyboard)
#     context.bot.send_message(
#         chat_id=chat.id,
#         text=(
#             'Чтобы удалить или отредактировать категорию, выберите ее ниже.'
#             'Будьте аккуратны: при удалении категории удаляются все записи'
#             'о доходах/расходах в данной категории.'
#         ),
#         reply_markup=reply_markup,
#     )


# def income_category_update(update, context):
#     """
#     Выводить кнопки для удаления или редактирования
#     выбранной категории и кнопки назад.
#     """
#     chat = update.effective_chat
#     query = update.callback_query
#     variant = query.data
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 'Изменить название категории',
#                 callback_data='update_category'
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 'Удалить категорию и все её записи',
#                 callback_data='delete_category'
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 'Назад',
#                 callback_data='incomes_category_update'
#             )
#         ],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     context.bot.send_message(
#         chat_id=chat.id,
#         text='Вы выбрали {}'.format(variant),
#         reply_markup=reply_markup,
#     )
