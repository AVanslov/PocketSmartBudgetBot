from django import forms

from bot.models import (
    Category,
    Money,
    UserMainCurrency,
)


class IncomeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(kwargs)
        
        author = kwargs['initial']['request']
        print(author)
        print(self.fields)
        print(vars(self.fields['type']))
        
        self.fields['category'].queryset = Category.objects.filter(
            author__id=author.id
        )

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # category = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Money
        fields = (
            'type',
            'date',
            'category',
            'value',
            'currency',
            'comment',
        )
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model=Category
        fields = (
            'type',
            'category',
            'limit',
        )


class UserMainCurrencyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserMainCurrency
        fields = (
            'main_currency',
        )
