FROM python:3.11-slim

WORKDIR /app

RUN pip install flask gunicorn

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
