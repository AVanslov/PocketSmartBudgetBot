from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CategoryAbstractModel(models.Model):
    """
    Абстрактная модель описывает таблицы категорий для доходов и расходов.
    """
    category = models.CharField(default=None, max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

    class Meta:
        abstract = True


class CategoryOfIncomes(CategoryAbstractModel):
    pass


class CategoryOfExpenses(CategoryAbstractModel):
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
        default_related_name = '%(class)s'


class Income(MoneyAbstractModel):
    category = models.ForeignKey(
        CategoryOfIncomes,
        on_delete=models.CASCADE,
    )
    # pass


class Expense(MoneyAbstractModel):
    category = models.ForeignKey(
        CategoryOfExpenses,
        on_delete=models.CASCADE,
    )
    # pass
