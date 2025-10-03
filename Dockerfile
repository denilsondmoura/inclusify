# Base Python slim
FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        gnupg \
        unzip \
        xvfb \
        libnss3 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libxkbcommon0 \
        libxss1 \
        libgbm1 \
        libasound2 \
        gcc \
        libpq-dev \
        chromium \
        chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}/app

# Copiar requirements
COPY requirements.txt /app/

# Copiar scripts de entrypoint
COPY ../scripts/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY ../scripts/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

# Instalar dependências Python
RUN pip install --upgrade pip \
    && pip install --root-user-action=ignore -r requirements.txt

# Entrypoint
ENTRYPOINT ["/entrypoint"]
