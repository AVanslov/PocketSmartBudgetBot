from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CategoriesAbstractModel(models.Model):
    """
    Абстрактная модель описывает таблицы категорий для доходов и расходов.
    """
    category = models.CharField(default=None, max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CategoriesOfIncomes(CategoriesAbstractModel):
    pass


class CategoriesOfExpenses(CategoriesAbstractModel):
    pass


class MoneyAbstractModel(models.Model):
    """
    Абстрактная модель описывает таблицы расходов и доходов.
    """
    comment = models.CharField(default=None, max_length=150)
    # category = models.CharField(max_length=150)
    value = models.IntegerField(default=0)
    date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:

        abstract = True


class Incomes(MoneyAbstractModel):
    category = models.ForeignKey(
        CategoriesOfIncomes,
        on_delete=models.CASCADE,
        related_name='incomes'
    )
    # pass


class Expenses(MoneyAbstractModel):
    category = models.ForeignKey(
        CategoriesOfExpenses,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    # pass
