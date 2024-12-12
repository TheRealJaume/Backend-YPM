# Dockerfile
# Imagen base con Python 3.10
FROM python:3.10-slim

# Configuración del entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo en el contenedor
WORKDIR /ypm

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && \
    apt-get clean

# Instalar dependencias del proyecto
COPY requirements.txt /ypm/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . /ypm/

# Exponer el puerto (si es necesario)
EXPOSE 8000

# Comando para iniciar el contenedor
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ypm.wsgi:application"]
