FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /budget_project

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

RUN python3 BudgetPlanerBot.py

CMD ["python", "manage.py", "runserver", "0:8000"] 

