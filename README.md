**EN**
# SIMBU - Online service for budget management and planning
The project is available at [simbu .zapto.org](https://simbu.zapto.org/)

## Overview
For proper budget management, it is necessary to be able to plan expenses and income and know at any given time how much money is available, as well as be able to distribute it competently and be able to analyze your assets and liabilities.
This is what the SIMBU service was created for. 
Here the user can record his expenses and income, create his own categories of expenses and income, add monetary transactions in any currency and display statistics in the selected main currency. At the same time, all calculations will be made taking into account the exchange rate on the day of the transaction, which allows you to accurately calculate the budget in any currency.

### Applied technologies
**Languages**
- Python
- HTML
- CSS
- JavaScript

**Frameworks**
- Django
- Bootstrap

**Libraries**
- matplotlib
- python-telegram-bot
- smart-select

**Data Base**
- SQlite for development
- PostgrsQL for production

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

## Project development plans

- [x] 04.24 - 05.24 - To work on the main errors in the code and configure CI/CD on a temporary server.  To test the service during personal use.
- [ ] 05.24 - 06.24 - 
Add a data import function. Create a user profile page. 
add the ability to create records in the future and automatically update the exchange rate as soon as information appears on the exchange on that date. 
Write graph construction in JavaScript.
Enable payment for registration.
Rewrite the telegram code of the bot and connect it to the service. 
Transfer the service to the DigitalOcean server.

**Author** Buchelnikov Aleksandr


**RU**

# SIMBU - Онлайн-сервис для управления и планирования бюджета

Проект доступен по адресу [simba .zapto.org](https://simba.zapto.org/)

## Обзор
Для правильного управления бюджетом необходимо уметь планировать расходы и доходы и знать, сколько денег доступно в любой момент времени, а также уметь грамотно распределять их и анализировать свои активы и пассивы.
Именно для этого и был создан сервис SIMBU. 
Здесь пользователь может записывать свои расходы и доходы, создавать свои собственные категории расходов и доходов, добавлять денежные транзакции в любой валюте и отображать статистику в выбранной основной валюте. При этом все расчеты будут производиться с учетом обменного курса на день совершения транзакции, что позволяет точно рассчитать бюджет в любой валюте.

### Применяемые технологии

**Языки**
- Python
- HTML
- CSS
- JavaScript

**Фреймворки**
- Django
- Bootstrap

**Библиотеки**
- matplotlib
- python-telegram-bot
- smart-select

**Базы данных**
- SQlite for development
- PostgrsQL for production

## Функционал и возможности приложения

Регистрация организована через приложение Auth, встроенное в Django.

После регистрации пользователь получает доступ к панели мониторинга. 
На главной странице панели мониторинга вы можете сразу увидеть все расходы и доход, добавить новый доход или расход, а также удалить или отредактировать существующий.
С помощью аннотации и агрегации суммы расходов и доходов за текущий месяц отображаются под таблицей с расходами и доходами.

В центре страницы находится таблица категорий, где пользователь может просмотреть все категории, которые он добавил, а также увидеть запланированные расходы/доходы, фактические расходы/доходы и разницу между ними для каждой категории. Кроме того, под таблицей отображаются фактические и планируемые суммы расходов и доходов за текущий месяц.
Для реализации этой функциональности был написан наиболее оптимизированный набор запросов с использованием аннотаций и агрегирования, а также:
Обертка выражений, подзапрос, F, Q, Объединение, Округление.

База данных состоит из таких таблиц, как type - в ней есть два поля Доходы и расходы, categories - для описания категорий доходов и расходов (эта таблица связана с таблицей типов как много один ко многим), money - таблица всех доходов и расходов - в ней так, чтобы пользователь видел только те категории, которые он добавил одновременно, если он выбирает тип дохода, в поле отображались только категории, где поле тип__название = доходы, а также с расходами используется библиотека интеллектуального выбора

На данный момент для реализации графиков используется библиотека Matplotlib, но в настоящее время я работаю над тем, чтобы все графики были реализованы на JavaScript - это позволит им быть адаптивными и интерактивными.

## Планы развития проекта

- [x] 04.24 - 05.24 - Работа над основными ошибками в коде и настройки CI/CD на временном сервере. Тестирование сервиса при личном использовании.
- [ ] 05.24 - 06.24 - 
Добавьте функцию импорта данных. Создайте страницу профиля пользователя. 
добавьте возможность создавать записи в будущем и автоматически обновлять обменный курс, как только на бирже появится информация на эту дату. 
Напишите построение графика на JavaScript.
Включите оплату за регистрацию.
Перепишите telegram-код бота и подключите его к сервису. 
Перенесите сервис на сервер DigitalOcean.

**Автор** Бучельников Александр
