from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MoneyAbstractModel(models.Model):
    """
    Абстрактная модель описывает таблицы расходов и доходов.
    """
    comment = models.CharField(default=None, max_length=150)
    category = models.CharField(max_length=150)
    value = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:

        abstract = True


class Incomes(MoneyAbstractModel):
    pass


class Expenses(MoneyAbstractModel):
    pass
