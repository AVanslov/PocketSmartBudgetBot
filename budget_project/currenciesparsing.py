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


def save_parsing_result_to_db(result):
    # перебрать в цикле словари из данных каждого словаря создать объект модели, но не сохранять
    # с помощью balk_create создать группу объектов

    #сначала проверить, что найденные курсы валют уже есть или создать новые в модель Currency
    
    currencies = []
    for i in result:
        currency, status =  Currency.objects.get_or_create(
            name = i['symbol'][0:3]
        )
        currencies.append(currency)
        currency, status =  Currency.objects.get_or_create(
            name = i['symbol'][3:6]
        )
        currencies.append(currency)
    
    objects = []
    for i in result:
        objects.append(
            Rate(
                date=today,
                first_currency = get_object_or_404(
                    Currency,
                    name=i['symbol'][3:6]
                ),
                second_currency = get_object_or_404(
                    Currency,
                    name=i['symbol'][:3]),
                rate=i['last_price']
            )
        )

    print([i.name for i in Currency.objects.all()])
    
    for i in Currency.objects.all():
        objects.append(
            Rate(
                date=today,
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

    Rate.objects.bulk_create(objects)
    # дальше во views будет вызов объектов модели Rate и получение объектов


def currency_parsing():
    """
    Делает запрос к серверу сервиса валют каждые 24 часа,
    возвращает json, далее нужно сохранить эти данные в БД.
    """
    # Мне нужен список валютных пар
    # ключ API
    # currencies=Currency.objects.all()
    # serialized_data = serialize("json", currencies)
    # serialized_data = json.loads(serialized_data)
    # serialized_data
    # pprint(serialized_data)
    # currencies_list = [i['fields']['name'] for i in serialized_data]
    # print(currencies_list)

    #генерируем пару значений
    # pairs = []
    # for i in currencies_list:
    #     for b in currencies_list:
    #         if b !=i:
    #             pair = i+b
    #             pairs.append(pair)
        
    # print(pairs)

    result = [
    {'change_percentage': 0.9291291032221816,
    'last_price': 116.992,
    'name': 'Euro / Serbian Dinar',
    'symbol': 'EURRSD',
    'ticker': 'EURRSD.FOREX'},
    {'change_percentage': 0.5202283693909404,
    'last_price': 108.263,
    'name': 'US Dollar / Serbian Dinar',
    'symbol': 'USDRSD',
    'ticker': 'USDRSD.FOREX'}]

    # url='https://api.profit.com/data-api/fundamentals/forex/peers/{pair}?token=f4b37128adcb46a1a9a29eec180739f9'.format(pair='EURRSD')


    # result = requests.get(url)


    # pprint(result.json())

    # print([i['last price'] for i in result.json()])
    save_parsing_result_to_db(result)
    # Timer(86400, currency_parsing).start()


currency_parsing()
# Rate.objects.all().delete()
# for i in range(20,32):
# Currency.objects.get(pk=32).delete()