FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . .

# Порт (для ясности, хотя Gunicorn слушает 8000)
EXPOSE 8000

# Команда будет переопределена в docker-compose.yml (gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
