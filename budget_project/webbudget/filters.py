from django import forms
import django_filters
from django_filters import DateRangeFilter,DateFilter
from django_filters.widgets import RangeWidget

from bot.models import Money


class MoneyFilter(django_filters.FilterSet):
    # date_range = DateRangeFilter(field_name='date')
    # date = DateRangeFilter(label='Date_Range')

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
            super(MoneyFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
            self.filters['type'].field.widget.attrs.update({'class': 'field-style'})

    date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'type': 'date',
        'class': 'field-style'
    }))


    class Meta:
        model = Money
        fields = [
            'type',
            # 'category',
            # 'date'
        ]
        # widgets = {
        #     'type': SelectMultiple(attrs={'class': 'custom-select'}),     
        # }
