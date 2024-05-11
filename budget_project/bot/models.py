from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.shortcuts import get_object_or_404
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

from queryable_properties.properties import queryable_property

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
    limit = models.IntegerField(default=None, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.category


class Currency(models.Model):
    """
    Модель описывает валюты доступные для выбора.
    """
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class UserMainCurrency(models.Model):
    """
    Модель описывает главную валюту, которую выбрал пользователь.
    """
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    main_currency = models.ForeignKey(Currency, default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return f'{self.author.username} - {self.main_currency.name}'
    
    def create_user_main_currency(sender, instance, created, **kwargs):
        if created:
            UserMainCurrency.objects.create(author=instance)
            print('****************')
            print('Profile created!')
            print('Default currency is EUR!')
            print('****************')

    post_save.connect(create_user_main_currency, sender=User)

    def update_user_main_currency(sender, instance, created, **kwargs):
        if created is False:
            instance.usermaincurrency.save()
            print('****************')
            print('Currency Updated!')
            print('****************')

    post_save.connect(update_user_main_currency, sender=User)


class Rate(models.Model):
    """
    Модель описывает курсы валют.
    """
    date = models.DateField()
    first_currency = models.ForeignKey(
        Currency,
        default=1,
        on_delete=models.SET_DEFAULT,
        related_name='rates_by_first_currency'
    )
    second_currency = models.ForeignKey(
        Currency,
        default=2,
        on_delete=models.SET_DEFAULT,
        related_name='rates_by_second_currency'
    )
    rate = models.FloatField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['date', 'first_currency', 'second_currency'],
                name='unique_%(class)s',
            ),
        ]


class Money(models.Model):
    """
    Модель описывает таблицы расходов и доходов.
    """
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    comment = models.CharField(default=None, max_length=150)
    category = GroupedForeignKey(
        Category,
        'type'
    )
    # category = ChainedForeignKey(
    #     Category,
    #     chained_field='type',
    #     chained_model_field='type',
    #     show_all=False,
    #     auto_choose=False,
    #     sort=True,
    # )
    value = models.IntegerField(default=0)
    date = models.DateField()
    currency = models.ForeignKey(Currency, default=1, on_delete=models.SET_DEFAULT)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.type.name
    
    @property
    def value_in_main_currency(self):
        print(self.currency.id)
        print(self.author.usermaincurrency.main_currency.id)
        return round(
            self.value / get_object_or_404(
                Rate,
                date=self.date,
                first_currency=self.author.usermaincurrency.main_currency.id,
                second_currency=self.currency.id
                # first_currency=self.currency.id,
                # second_currency=self.author.usermaincurrency.main_currency.id
            ).rate,
            2
        )


    class Meta:
        default_related_name = '%(class)s'
        ordering = ('-date',)

    
