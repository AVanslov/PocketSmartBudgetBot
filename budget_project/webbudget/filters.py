import django_filters
from bot.models import Income


class IncomeFilter(django_filters.FilterSet):

    class Meta:
        model = Income
        fields = [
            'category',
        ]
