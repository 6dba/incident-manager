FROM python:3.12-slim

# Инициализация ядра
WORKDIR /usr/src/app/core
COPY core .
RUN pip install --no-cache-dir -r requirements.txt

# Инициализация сервиса
WORKDIR /usr/src/app/services
COPY services/__init__.py .

WORKDIR /usr/src/app/services/processor
COPY services/processor .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
COPY .env .

CMD [ "python", "-m", "services.processor.main" ]

LABEL authors="sixsixsix"
