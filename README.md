# SIMBU - Online service for budget management and planning

## Overview
For proper budget management, it is necessary to be able to plan expenses and income and know at any given time how much money is available, as well as be able to distribute it competently and be able to analyze your assets and liabilities.
This is what the SIMBU service was created for. 
Here the user can record his expenses and income, create his own categories of expenses and income, add monetary transactions in any currency and display statistics in the selected main currency. At the same time, all calculations will be made taking into account the exchange rate on the day of the transaction, which allows you to accurately calculate the budget in any currency.

### Applied technologies

**Frameworks**
Django
Bootstrap

**Libraries**
matplotlib
python-telegram-bot
smart-select

## Functionality and features of the application

Registration is organized through the Auth application built into Django.

After registration, the user has access to the dashboard. 
On the dashboard's main page, you can immediately see all expenses and income, add a new income or expense, or delete or edit an existing one.
With the help of annotation and aggregation, the amounts of expenses and income for the current month are displayed under the table with expenses and income.

In the center of the page there is a category table where the user can see all the categories that he has added, as well as see the planned expenses / income, actual expenses/ income and the difference between them for each category. In addition, the actual and planned amounts of expenses and income for the current month are displayed under the table.
To implement this functionality, the most optimized Query set was written using annotation and aggregation, as well as:
ExpressionWrapper, Subquery, F, Q, Coalesce, Round.

The database consists of tables such as type - it has two fields Incomes and expenses, categories - to describe categories of income and expenses (this table is linked to the table of types as many one to many), money - a table of all income and expenses - in it so that the user sees only those categories that he added at the same time, if he chooses the income type, only categories were displayed in the field, where the type__name = incomes field, and also with expenses, the smart-select library is used

At the moment, the Matplotlib library is used to implement graphs, but I am currently working to ensure that all graphs are implemented in JavaScript - this will allow them to be adaptive and interactive.





### RU
После регистрации у пользователя появляется доступ к дашборду. На главной странице дашборда можно сразу увидеть все расходы и доходы, добавить новый доход или расход или удалить или отредактировать существующий.
С помощью аннотации и агрегации под таблицей с расходами и доходами выводятся суммы расходов и доходов за текущий месяц.

В центре страницы расположена таблица категорий, где пользователь может увидеть все категории, которые он добавил, а также увидеть планируемы расходы / доходы, фактические расходы/ доходы и разницу между ними для каждой категории. Помимо этого под таблицей выводятся суммы расходов и доходов фактические и планируемые за текущий месяц.
Для реализации этого функционала были написаны максимально оптимизированный запрос Query set с использованием аннотации и агрегации, а также:
ExpressionWrapper, Subquery, F, Q, Coalesce, Round.

Для реализации графиков на данный момент используется библиотека Matplotlib, однако я сейчас работаю над тем чтобы все графики были реализованы на JavaScript - это позволит им быть адаптивными и интерактивными.

Запуск сервиса c PostgreSQL

если запускать из локального образа:
sudo docker compose stop && sudo docker compose up --build

если запускать из образа dockerhub:
docker compose -f docker-compose.production.yml up

Открыть новое окно терминала

sudo docker compose exec budget_project python3 manage.py makemigrations

sudo docker compose exec budget_project python3 manage.py migrate

sudo docker compose exec budget_project python3 BudgetPlanerBot.py