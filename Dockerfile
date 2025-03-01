FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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