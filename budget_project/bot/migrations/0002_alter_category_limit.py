# Generated by Django 4.2 on 2024-05-23 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='limit',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
