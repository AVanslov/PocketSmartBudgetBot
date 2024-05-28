"""
Модуль для операций с базой данных во время разработки.
"""

import django

import os

from django.shortcuts import get_object_or_404

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_project.settings')
django.setup()

from bot.models import Currency, Rate, Money

Rate.objects.all().delete()