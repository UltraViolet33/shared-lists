# === BASE STAGE (Common Dependencies) ===
FROM python:3-alpine as base

WORKDIR /usr/src/app

COPY requirements.txt .

RUN \
    apk add --no-cache python3 postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps


# === DEVELOPMENT STAGE ===
FROM base AS dev

ENV FLASK_ENV=development
ENV FLASK_APP=app.py
ENV PATH="/venv/bin:$PATH"

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# === PRODUCTION STAGE ===
FROM base AS prod

ENV FLASK_ENV=production
ENV FLASK_APP=app.py
ENV PATH="/venv/bin:$PATH"

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
