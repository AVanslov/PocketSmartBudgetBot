from datetime import date, datetime, timedelta
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


TODAY = date.today()

# START_DATE='2024-01-01'
START_DATE=date(2024, 1, 1)

API_KEY='IgkovF8sB6vAxLk5meZ5BtXZ8bwXUONG'

CURRENCIES = [
    'C:EURRSD',
    'C:USDRSD',
    'C:USDEUR',
    'C:EURRUB',
    'C:USDRUB',
]


def save_parsing_result_to_db(result, date):
    # перебрать в цикле словари из данных каждого словаря создать объект модели, но не сохранять
    # с помощью balk_create создать группу объектов


    usefull_rates = [i for i in result.json()['results'] if i['T'] in CURRENCIES]


    for i in usefull_rates:
        Currency.objects.get_or_create(
            name = i['T'][2:5]
        )
        Currency.objects.get_or_create(
            name = i['T'][5:8]
        )
    
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
                rate=1.19
            )
        )
    objects.append(
            Rate(
                date=date,
                first_currency=get_object_or_404(
                    Currency,
                    name='RSD'
                ),
                second_currency=get_object_or_404(
                    Currency,
                    name='RUB'
                ),
                rate=0.84
            )
        )

    Rate.objects.bulk_create(objects)
    # дальше во views будет вызов объектов модели Rate и получение объектов


def currency_parsing():
    """
    Делает запрос к серверу сервиса валют каждые 24 часа,
    возвращает json, отправляет данные на сохранение в БД.
    """

    # date='2024-05-10' # для ручного тестирования

    # запрос всех доступных пар на указанный день

    url='https://api.polygon.io/v2/aggs/grouped/locale/global/market/fx/{date}?adjusted=true&apiKey={api_key}'.format(
        date=TODAY,
        api_key=API_KEY,
    )

    result = requests.get(url)

    pprint(result.json())

    save_parsing_result_to_db(result, date=TODAY)
    # Timer(86400, currency_parsing).start() # запуск фукции каждые 24 часа


def save_historical_rates_to_db(result, pair):
    """
    Получет JSON с курсами валют за указанный промежуток времени,
    Проверяет, чтобы таких курсов уже не было и пропускает значения,
    если они уже есть для данной пары,
    Сохраняет данные в БД.
    """
    # получаем словарь с ключами:

    # 'ticker': 'C:EURUSD'

    # 'results' - содержит список словарей,

    # нас интересуют ключи:
    # 't' - временной штамп
    # 'vw' - курс валюты

    first_currency = pair[2:5]
    second_currency = pair[5:8]

    objects = []
    for currency_on_day in result.json()['results']:
        current_date = datetime.fromtimestamp(currency_on_day['t']/1000)
        if not Rate.objects.filter(
            date=current_date,
            first_currency__name=first_currency,
            second_currency__name=second_currency,
        ).exists():
            objects.append(
                Rate(
                    date=current_date,
                    first_currency=get_object_or_404(
                        Currency,
                        name=first_currency
                    ),
                    second_currency=get_object_or_404(
                        Currency,
                        name=second_currency
                    ),
                    rate=currency_on_day['vw']
                )
            )
        if not Rate.objects.filter(
            date=current_date,
            first_currency__name=first_currency,
            second_currency__name=first_currency,
        ).exists():
            objects.append(
                Rate(
                    date=current_date,
                    first_currency=get_object_or_404(
                        Currency,
                        name=first_currency
                    ),
                    second_currency=get_object_or_404(
                        Currency,
                        name=first_currency
                    ),
                    rate=1
                )
            )
        if not Rate.objects.filter(
            date=current_date,
            first_currency__name=second_currency,
            second_currency__name=second_currency,
        ).exists():
            objects.append(
                Rate(
                    date=current_date,
                    first_currency=get_object_or_404(
                        Currency,
                        name=second_currency
                    ),
                    second_currency=get_object_or_404(
                        Currency,
                        name=second_currency
                    ),
                    rate=1
                )
            )

    Rate.objects.bulk_create(objects)

def save_rub_rsd_to_db(start_date, end_date):
    # вручную допишем для пары RUBRSD
    delta = timedelta(days=1)
    days = []

    while start_date <= end_date:
        days.append(start_date)
        start_date += delta
    
    print(f'Days between {start_date} and {end_date}')
    print(days)

    objects = []
    for current_date in days:
        if not Rate.objects.filter(
            date=current_date,
            first_currency__name='RUB',
            second_currency__name='RSD',
        ).exists():
            objects.append(
                Rate(
                    date=current_date,
                    first_currency=get_object_or_404(
                        Currency,
                        name='RUB'
                    ),
                    second_currency=get_object_or_404(
                        Currency,
                        name='RSD'
                    ),
                    rate=1.19
                )
            )
        if not Rate.objects.filter(
            date=current_date,
            first_currency__name='RSD',
            second_currency__name='RUB',
        ).exists():
            objects.append(
                Rate(
                    date=current_date,
                    first_currency=get_object_or_404(
                        Currency,
                        name='RSD'
                    ),
                    second_currency=get_object_or_404(
                        Currency,
                        name='RUB'
                    ),
                    rate=0.84
                )
            )
    Rate.objects.bulk_create(objects)


def historical_rates(start_date, end_date, pair):
    """
    Получает историю курсов валют за указанный период времени,
    Отправляет полученные данные на сохранение в БД.
    """
    url = 'https://api.polygon.io/v2/aggs/ticker/{pair}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&apiKey={api_key}'.format(
        pair=pair, # значение вида C:EURUSD
        start_date=start_date,
        end_date=end_date,
        api_key=API_KEY,
    )
    result = requests.get(url)

    pprint(result.json())

    save_historical_rates_to_db(result, pair)




print(f'The code has been started at {datetime.now()}')

currency_parsing()

print(f'All data for {TODAY} has been successfully added at {datetime.now()}')

# не забываем, что текщий лимит тарифа 5 API Calls / Minute - более 5 объектов в списке за раз не передавать

for current_pair in CURRENCIES:
    historical_rates(start_date=START_DATE, end_date=TODAY, pair=current_pair)
    print(f'All data from {START_DATE} to {TODAY} has been successfully added at {datetime.now()}')

save_rub_rsd_to_db(start_date=START_DATE, end_date=TODAY)
print(f'All data for RUB and RSD from {START_DATE} to {TODAY} has been successfully added at {datetime.now()}')