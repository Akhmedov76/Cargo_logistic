FROM python:3.12
LABEL maintainer="cargo"

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]

