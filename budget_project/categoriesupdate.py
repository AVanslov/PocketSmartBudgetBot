from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot import views


def list_of_author_categories(type: str, author):
    """
    Принимает тип incomes/expenses
    возвращает список с категориями данного типа.
    """
    categories = []
    if type == 'incomes':
        for i in views.get_income_categories(author):
            categories.append(i['category'])
    else:
        for i in views.get_expense_categories(author):
            categories.append(i['category'])
    return categories


def inline_categories_buttons(type: str, author):
    """
    Принимает объект chat для получения информации об авторе
    и тип incomes/expenses
    Возвращает список со списками,
    [
        [
            InlineKeyboardButton(
                'Название категории',
                callback_data='type, ID категории',
            ),
        ],
    ].
    """
    keyboard = []
    if type == 'incomes':
        for i in views.get_income_categories(author):
            list = []
            list.append(
                    InlineKeyboardButton(
                        i['category'],
                        callback_data=i['category']
                    )
                )
            keyboard.append(list)
    else:
        for i in views.get_expense_categories(author):
            list = []
            list.append(
                    InlineKeyboardButton(
                        i['category'],
                        callback_data=i['category']
                    )
                )
            keyboard.append(list)
    print(views.get_income_categories(author))
    print(keyboard)
    return keyboard


def incomes_category_update(update, context):
    """
    Выводит inline кнопки с категориями
    Также показывает кнопки создать категорию и удалить все категории
    Показывает надпись - чтобы отредактировать существующую категорию, нажмите на нее ниже.
    """
    chat = update.effective_chat
    keyboard = inline_categories_buttons(type='income', author=chat) # функция, которая возвращает inline кнопки с категориями
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat.id,
        text='Чтобы удалить или отредактировать категорию, выберите ее ниже.',
        reply_markup=reply_markup,
    )
