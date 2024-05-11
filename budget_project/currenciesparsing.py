from datetime import date
import django
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.shortcuts import get_object_or_404
import requests
import os
from pprint import pprint
from threading import Timer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_project.settings')
django.setup()

from bot.models import Currency, Rate



today = date.today()

# написать функцию, которая загрузит при деплое данные за последний год

def save_parsing_result_to_db(result, date):
    # перебрать в цикле словари из данных каждого словаря создать объект модели, но не сохранять
    # с помощью balk_create создать группу объектов

    #сначала проверить, что найденные курсы валют уже есть или создать новые в модель Currency
    # date = today
    # print(date)

    currencies = [
        'C:EURRSD',
        'C:USDRSD',
        'C:USDEUR',
        'C:EURRUB',
        'C:USDRUB',
    ]

    usefull_rates = [i for i in result.json()['results'] if i['T'] in currencies]


    currencies = []
    for i in usefull_rates:
        currency, status =  Currency.objects.get_or_create(
            name = i['T'][2:5]
        )
        currencies.append(currency)
        currency, status =  Currency.objects.get_or_create(
            name = i['T'][5:8]
        )
        currencies.append(currency)
    
    objects = []
    for i in usefull_rates:
        objects.append(
            Rate(
                date=date,
                first_currency = get_object_or_404(
                    Currency,
                    name=i['T'][2:5]
                ),
                second_currency = get_object_or_404(
                    Currency,
                    name=i['T'][5:8]),
                rate=i['vw']
            )
        )
        objects.append(
            Rate(
                date=date,
                first_currency = get_object_or_404(
                    Currency,
                    name=i['T'][5:8]
                ),
                second_currency = get_object_or_404(
                    Currency,
                    name=i['T'][2:5]),
                rate=1/i['vw']
            )
        )

    print([i.name for i in Currency.objects.all()])
    
    for i in Currency.objects.all():
        objects.append(
            Rate(
                date=date,
                first_currency=get_object_or_404(
                    Currency,
                    name=i.name
                ),
                second_currency=get_object_or_404(
                    Currency,
                    name=i.name
                ),
                rate=1
            )
        )

    # вручную допишем для пары RUBRSD
    objects.append(
            Rate(
                date=date,
                first_currency=get_object_or_404(
                    Currency,
                    name='RUB'
                ),
                second_currency=get_object_or_404(
                    Currency,
                    name='RSD'
                ),
                rate=1
            )
        )

    Rate.objects.bulk_create(objects)
    # дальше во views будет вызов объектов модели Rate и получение объектов


def currency_parsing():
    """
    Делает запрос к серверу сервиса валют каждые 24 часа,
    возвращает json, далее нужно сохранить эти данные в БД.
    """

    # url='https://api.profit.com/data-api/fundamentals/forex/peers/{pair}?token=f4b37128adcb46a1a9a29eec180739f9'.format(pair=pair)

    # currency_pair='EURRSD'
    # start_date='2023-01-09'
    date='2024-01-11'
    # end_date='2023-01-09'
    api_key='IgkovF8sB6vAxLk5meZ5BtXZ8bwXUONG'

    # запрос всех доступных пар на указанный день

    url='https://api.polygon.io/v2/aggs/grouped/locale/global/market/fx/{date}?adjusted=true&apiKey={api_key}'.format(
        # currency_pair=currency_pair,
        date=date,
        api_key=api_key,
    )

    result = requests.get(url)

    pprint(result.json())


    # print([i['last price'] for i in result.json()])
    save_parsing_result_to_db(result, date)
    # Timer(86400, currency_parsing).start()


currency_parsing()
# Rate.objects.all().delete()
# for i in range(20,32):
# Currency.objects.get(pk=32).delete()