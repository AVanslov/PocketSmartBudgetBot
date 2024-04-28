from django import forms

from bot.models import Category, Money


class IncomeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'field-style'

    class Meta:
        model = Money
        fields = (
            'type',
            'date',
            'category',
            'value',
            'comment',
        )
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
