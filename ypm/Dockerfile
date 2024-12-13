# Etapa 1: Construcción de dependencias
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /ypm

RUN apt-get update && apt-get install -y build-essential libpq-dev && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Etapa 2: Imagen final
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /ypm

COPY --from=builder /install /usr/local
COPY . .

RUN apt-get update && apt-get install -y libpq-dev

EXPOSE 8000

CMD ["gunicorn", "--workers", "5", "--threads", "2", "--bind", "0.0.0.0:8000", "ypm.wsgi:application"]
