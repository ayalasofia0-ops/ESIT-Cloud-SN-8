# Usar imagen base de Python 3.11
FROM python:3.13-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    git \
    ca-certificates \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js 18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV REFLEX_BACKEND_PORT=8000
ENV NODE_ENV=production

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["sh", "-c", "reflex init && reflex run --env prod --backend-only --loglevel info"]