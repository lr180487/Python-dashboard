FROM python:3.12-alpine

# Variables optimización
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio trabajo
WORKDIR /app

# Dependencias del sistema
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev

# Copiar requirements primero
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

# Puerto
EXPOSE 8000

# Ejecutar
CMD ["python", "app.py"]