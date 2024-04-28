import django_filters
from bot.models import Money


class MoneyFilter(django_filters.FilterSet):

    class Meta:
        model = Money
        fields = [
            'type',
            'category',
        ]
