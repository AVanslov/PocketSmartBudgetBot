FROM python:3.9

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /app/budget_project

# RUN python3 manage.py makemigrations

# RUN python3 manage.py migrate

# RUN python3 BudgetPlanerBot.py

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "budget_project.wsgi"] 

