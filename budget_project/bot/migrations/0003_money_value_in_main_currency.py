# Generated by Django 4.2 on 2024-05-09 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_money_currency_rate_first_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='money',
            name='value_in_main_currency',
            field=models.FloatField(default=0),
        ),
    ]
