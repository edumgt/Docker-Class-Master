FROM python:3.12-alpine

WORKDIR /app
COPY server.py /app/server.py

RUN apk add --no-cache postgresql-client mariadb-client \
    && adduser -D app

USER app

EXPOSE 9000
CMD ["python", "/app/server.py"]
