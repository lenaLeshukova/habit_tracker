FROM python:3.12-slim

# Системные настройки
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=true

# Настраиваем жесткий путь к виртуальному окружению, которое создаст Poetry
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Устанавливаем системные зависимости для компиляции пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://python-poetry.org | python3 -

# Копируем конфигурационные файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Говорим Poetry создать виртуальное окружение именно по нашему пути /opt/venv
RUN poetry config virtualenvs.path /opt/virtualenvs \
    && python -m venv $VIRTUAL_ENV \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем весь остальной код проекта
COPY . .

EXPOSE 8000
