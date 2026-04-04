FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Agent/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY Agent/backend ./backend

EXPOSE 8080
ENV PORT=8080
ENV ENV=production

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
