FROM python:3.13-slim

#Configurar variables de entorno,
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Establecer directorio de trabajo,
WORKDIR /usr/app

#Instalar dependencias del sistema,
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#Instalar dependencias de Python,
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copiar el proyecto,
COPY . .

#Exponer puerto,
EXPOSE 9217

#Comando para iniciar la aplicación,
CMD ["python", "manage.py", "runserver", "0.0.0.0:9217"]