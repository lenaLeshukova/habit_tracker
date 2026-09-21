FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry"

# Явно прописываем пути к бинарникам Poetry и установленным пакетам
ENV PATH="/root/.local/bin:$POETRY_HOME/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry напрямую через pip
RUN pip install --no-cache-dir poetry

# Копируем конфигурацию зависимостей проекта
COPY pyproject.toml poetry.lock* ./

# Отключаем создание venv и ставим пакеты напрямую
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем остальной код
COPY . .

EXPOSE 8000
