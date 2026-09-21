FROM python:3.12-slim

# Системные настройки для вывода логов Python без задержек
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Устанавливаем системные зависимости для работы базы данных PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем сгенерированный пайплайном requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости из файла + принудительно доставляем celery и redis
# прямо в глобальную область видимости контейнера
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir celery redis \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код проекта
COPY . .

EXPOSE 8000
