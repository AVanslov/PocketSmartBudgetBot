import django

import os

from django.shortcuts import get_object_or_404

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_project.settings')
django.setup()

from bot.models import Currency, Rate, Money

# Rate.objects.all().delete()
# for i in range(19,26):
#     Currency.objects.filter(id=i).delete()

# for i in range(1,11):
#     Money.objects.filter(id=i).delete()



# currencies = [
#         'C:EURRSD',
#         'C:USDRSD',
#         'C:USDEUR',
#         'C:EURRUB',
#         'C:USDRUB',
#     ]
# print([str(i[2:5])+','+str(i[5:8]) for i in currencies])

# def currencies_grafic():
#     """
#     Выводит график по стоимости всех валют относительно EUR.
#     """
#     currencies_list = [i.name for i in Currency.objects.all()]


        
#     data = [[rate.rate for rate in Rate.objects.filter(first_currency__name='EUR', second_currency__name=i.name).order_by('date')] for i in Currency.objects.all()]
#     dates = [[rate.date for rate in Rate.objects.filter(first_currency__name='EUR', second_currency__name=i.name).order_by('date')] for i in Currency.objects.all()]

#     print(data)
#     print(dates)

# currencies_grafic()
