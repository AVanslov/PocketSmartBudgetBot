from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bot.models import (
    CategoryOfIncomes,
    Income,
    Expense,
)
from .forms import IncomeForm


@login_required
def dashboard(request):

    title = 'Dashboard'
    # all_incomes = Income.objects.all()
    all_incomes = Income.objects.filter(author=request.user).order_by('-date')
    categories = CategoryOfIncomes.objects.all()
    # all_expenses = Expense.objects.filter(author=request.user)
    form = IncomeForm(request.POST or None)
    context = {
        'title': title,
        # 'products': products,
        'all_incomes': all_incomes,
        'categories': categories,
        # 'expenses': all_expenses,
        'form': form
    }
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        form.save()
    return render(request, 'webbudget/dashboard.html', context)
