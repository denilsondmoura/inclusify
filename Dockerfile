FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       wget \
       gnupg \
       unzip \
       xvfb \
       libnss3 \
       libgconf-2-4 \
       libatk1.0-0 \
       libatk-bridge2.0-0 \
       libcups2 \
       libxkbcommon0 \
       libxss1 \
       libgbm1 \
       libasound2 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
         > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

ARG CHROMEDRIVER_VERSION=136.0.7103.94

RUN wget -O /tmp/chromedriver.zip \
        "https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.94/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /usr/local/bin/chromedriver-linux64

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}/app

COPY requirements.txt /app/

COPY ../scripts/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ../scripts/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

RUN apt-get update -y && apt-get install -y gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install --root-user-action=ignore -r requirements.txt

ENTRYPOINT [ "/entrypoint" ]