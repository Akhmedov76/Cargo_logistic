FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    gettext-base \
    gettext \
    binutils \
    libproj-dev \
    gcc \
    libpq-dev \
    python3-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# entrypoint.sh ni qo'shish va ruxsat berish
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000 7009
