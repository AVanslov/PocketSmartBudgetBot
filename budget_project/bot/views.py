# Получаем, изменяем и записываем все данные в базу данных с помощью CRUD операций
from .models import (
    Incomes,
    Expenses,
    User,
)


def get_or_create_user(update_object):
    """
    Получает объект на основе update.effective_chat
    и создает объект модели User
    поля password и email формируются на основе id
    Используется только при первом входе в бот.

    Проверяет совпадает ли данные из объекта с update.effective_chat
    и возвращает объект User для предоставления права просматривать поля
    только этого пользователя.
    """
    new_user = User.objects.get_or_create(
        username=update_object.username,
        email=str(update_object.id) + '@budgetbot.com',
    )
    return new_user


def save_income_in_db(comment, category, value, author):
    """Добавляет запись о доходах в таблицу Incomes."""
    new_income = Incomes.objects.create(
        comment=comment,
        category=category,
        value=value,
        author=get_or_create_user(author)[0],
    )
    return new_income.save()


def save_expense_in_db(comment, category, value, author):
    """Добавляет запись о расходах в таблицу Expenses."""
    new_expence = Expenses.objects.create(
        comment=comment,
        category=category,
        value=value,
        author=get_or_create_user(author)[0]
    )
    return new_expence.save()


def get_report(author):
    """
    Получает все записи из таблицы Incomes
    и возвращает словари вложенные в список.
    """
    incomes = Incomes.objects.filter(author=get_or_create_user(author)[0])
    # print(incomes)
    # expenses = Expenses.objects.filter(author=get_or_create_user(author))
    list = []
    for income in incomes.values():
        list.append(income)
    # list.append(incomes)
    # list.append(expenses)
    return list


def get_report_expenses(author):
    """
    Получает все записи из таблицы Expenses
    и возвращает словари вложенные в список.
    """
    # incomes = Incomes.objects.filter(author=get_or_create_user(author)[0])
    # # print(incomes)
    expenses = Expenses.objects.filter(author=get_or_create_user(author)[0])
    list = []
    for expense in expenses.values():
        list.append(expense)
    # list.append(incomes)
    # list.append(expenses)
    return list


def delete_all(author):
    """
    Получает объект update.effective_chat
    удаляет все записи текущего пользователя
    возвращает пустой список записей текущего пользователя.
    """
    Incomes.objects.filter(author=get_or_create_user(author)[0]).delete()
    # Expenses.objects.filter(author=get_or_create_user(author)[0]).delete()
    return get_report(author)


def delete_all_expenses(author):
    """
    Получает объект update.effective_chat
    удаляет все записи текущего пользователя
    возвращает пустой список записей текущего пользователя.
    """
    # Incomes.objects.filter(author=get_or_create_user(author)[0]).delete()
    Expenses.objects.filter(author=get_or_create_user(author)[0]).delete()
    return get_report_expenses(author)
