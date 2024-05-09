import django

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_project.settings')
django.setup()

from bot.models import Currency, Rate

Rate.objects.all().delete()