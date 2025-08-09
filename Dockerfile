FROM python:3.11-slim

WORKDIR /social

# Tizim paketlarini o'rnatamiz
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Python muhit o'zgaruvchilarini sozlaymiz
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# requirements.txt ni konteynerga nusxalaymiz
COPY requirements.txt .

# Loyiha talablarini o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini konteynerga nusxalaymiz
COPY . .

# Statik fayllarni yig'ish
RUN python manage.py collectstatic --noinput

# Sinov uchun runserver yoki daphne tanlash uchun moslash
CMD ["sh", "-c", "if [ \"$RUNSERVER\" = \"true\" ]; then python manage.py runserver 0.0.0.0:$PORT; else daphne -b 0.0.0.0 -p $PORT social.asgi:application; fi"]