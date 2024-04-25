# Получаем, изменяем и записываем все данные в базу данных с помощью CRUD операций
from .models import (
    CategoriesOfExpenses,
    CategoriesOfIncomes,
    Incomes,
    Expenses,
    User,
)

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


def get_or_create_user(update_object):
    """
    Получает объект на основе update.effective_chat
    и создает объект модели User
    поля password и email формируются на основе id
    Используется только при первом входе в бот.

    Проверяет совпадает ли данные из объекта с update.effective_chat
    и возвращает объект User для предоставления права просматривать поля
    только этого полget_expenses_categoriesьзователя.
    """
    # если пользователь не существует,
    # создать два перечня категорий
    if User.objects.filter(
        username=update_object.id,
        email=str(update_object.id) + '@budgetbot.com',
    ).exists():
        new_user = User.objects.get_or_create(
            username=update_object.id,
            email=str(update_object.id) + '@budgetbot.com',
        )
    else:
        new_user = User.objects.get_or_create(
            username=update_object.id,
            email=str(update_object.id) + '@budgetbot.com',
        )

        incomes_categories = []
        for i in INCOMES_CATEGORIES_LIST:
            incomes_categories.append(
                CategoriesOfIncomes(
                    category=i,
                    author=new_user[0]
                )
            )
        CategoriesOfIncomes.objects.bulk_create(
            incomes_categories
        )

        expenses_categories = []
        for i in EXPENSES_CATEGORIES_LIST:
            expenses_categories.append(
                CategoriesOfIncomes(
                    category=i,
                    author=new_user[0]
                )
            )
        CategoriesOfExpenses.objects.bulk_create(
            expenses_categories
        )
    return new_user


def get_category_object(type: str, category, author):
    """
    Возвращает id искомой категории.
    """
    if type == 'incomes':
        category = CategoriesOfIncomes.objects.get(
            category=category,
            author=get_or_create_user(author)[0],
        )
        print(category.id)
    else:
        category = CategoriesOfExpenses.objects.get(
            category=category,
            author=get_or_create_user(author)[0],
        )
    return category.id


def save_income_in_db(comment, category, value, date, author):
    """Добавляет запись о доходах в таблицу Incomes."""
    new_income = Incomes.objects.create(
        comment=comment,
        category=CategoriesOfIncomes.objects.get(id=category), #collbackquery это id категории
        value=value,
        date=date,
        author=get_or_create_user(author)[0],
    )
    return new_income.save()


def save_expense_in_db(comment, category, value, date, author):
    """Добавляет запись о расходах в таблицу Expenses."""
    new_expence = Expenses.objects.create(
        comment=comment,
        category=CategoriesOfExpenses.objects.get(id=category),
        value=value,
        date=date,
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
    print(get_or_create_user(author)[0])
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


def create_income_category(category, author):
    category = CategoriesOfIncomes.objects.create(
        category=category,
        author=get_or_create_user(author)[0],
    )
    return category.save()


def create_expense_category(category, author):
    category = CategoriesOfExpenses.objects.create(
        category=category,
        author=get_or_create_user(author)[0],
    )
    return category.save()


def get_income_categories(author):
    """
    Возвращает категории доходов пользователя
    в виде cловарей, влоенных в список.
    """
    categories = CategoriesOfIncomes.objects.filter(
        author=get_or_create_user(author)[0]
    )
    list = []
    for category in categories.values():
        list.append(category)
    return list


def get_expense_categories(author):
    """
    Возвращает категории расходов пользователя
    в виде cловарей, влоенных в список.
    """
    categories = CategoriesOfExpenses.objects.filter(
        author=get_or_create_user(author)[0]
    )
    list = []
    for category in categories.values():
        list.append(category)
    return list


def delete_category(type: str, category, author):
    """
    Удаляет выбранную категорию.
    """
    CategoriesOfIncomes.objects.filter(
        category=category,
        author=get_or_create_user(author)[0]
    ).delete()
