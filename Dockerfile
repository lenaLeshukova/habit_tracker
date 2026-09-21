FROM python:3.12-slim

# Системные настройки для вывода логов без задержек
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Устанавливаем системные зависимости для сборки пакетов базы данных
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем конфигурационные файлы проекта
COPY pyproject.toml poetry.lock* ./

# Используем стандартный движок сборки, чтобы pip установил зависимости
# напрямую из pyproject.toml без генерации промежуточных requirements.txt файлов
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry-core \
    && pip install --no-cache-dir .

# Копируем весь остальной код вашего трекера полезных привычек
COPY . .

EXPOSE 8000
