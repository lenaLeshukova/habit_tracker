FROM python:3.12-slim

# Системные настройки
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Устанавливаем системные зависимости для работы базы данных
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем саму утилиту poetry через pip
RUN pip install --no-cache-dir poetry

# Копируем конфигурационные файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Отключаем создание виртуального окружения Poetry внутри докера,
# чтобы все пакеты ставились прямо в системный Python контейнера
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем весь остальной код проекта
COPY . .

# Открываем порт для Django
EXPOSE 8000
