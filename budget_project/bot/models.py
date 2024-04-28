from django.contrib.auth import get_user_model
from django.db import models
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey

User = get_user_model()


class Type(models.Model):
    name = models.CharField(default='income', max_length=10)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель описывает таблицы категорий для доходов и расходов.
    """
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.CharField(default=None, max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.category


class Money(models.Model):
    """
    Модель описывает таблицы расходов и доходов.
    """
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    comment = models.CharField(default=None, max_length=150)
    category = ChainedForeignKey(
        Category,
        chained_field='type',
        chained_model_field='type',
        show_all=False,
        auto_choose=False,
        sort=True,
    )
    value = models.IntegerField(default=0)
    date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.type.name

    class Meta:
        default_related_name = '%(class)s'
