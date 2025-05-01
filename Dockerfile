FROM python:3.12-slim

WORKDIR /code

# Встановлюємо netcat + pg_isready
RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
