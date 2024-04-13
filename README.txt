# Запуск сервиса c PostgreSQL

если запускать из локального образа:
sudo docker compose stop && sudo docker compose up --build

если запускать из образа dockerhub:
docker compose -f docker-compose.production.yml up

Открыть новое окно терминала

sudo docker compose exec budget_project python3 manage.py makemigrations

sudo docker compose exec budget_project python3 manage.py migrate

sudo docker compose exec budget_project python3 BudgetPlanerBot.py