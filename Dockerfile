# Frontend Build Stage
FROM node:12 as frontend-builder

RUN mkdir -p /app/tmp/build
RUN mkdir -p /app/tmp/build/public/sass
COPY ./package.json /app/tmp/build
COPY ./package-lock.json /app/tmp/build
COPY ./public/sass /app/tmp/build/public/sass
WORKDIR /app/tmp/build

RUN npm install
RUN npm run build # css files should be in /app/tmp/build/public/css

# Build Stage
FROM python:3.8.6-alpine3.12 as builder


RUN apk add --update \
    postgresql-dev   \
    gcc              \
    g++              \
    musl-dev         \
    linux-headers    \
    libffi-dev

# Build deps
WORKDIR /wheels
COPY ./requirements.txt /wheels
RUN pip install -U pip && pip wheel -r ./requirements.txt

# FROM python:3.8.6-alpine3.12

# Install wait-for-it for docker-compose
# so that we can wait for the database to
# startup if we need to.
RUN apk add --update curl
RUN curl -s https://raw.githubusercontent.com/eficode/wait-for/master/wait-for \
    -o /usr/local/bin/wait-for && \
  chmod +x /usr/local/bin/wait-for

# COPY --from=builder /wheels /wheels

RUN pip install -U pip && \
    pip install \
        -r /wheels/requirements.txt \
        -f /wheels && \
    rm -rf /wheels  && \
    rm -rf /root/.cache/pip/*

# RUN mkdir -p /usr/local/lib/python3.8/site-packages/
# COPY --from=builder /usr/local/lib/python3.8/site-packages/_brotli.cpython-38-x86_64-linux-gnu.so /usr/local/lib/python3.8/site-packages/_brotli.cpython-38-x86_64-linux-gnu.so


# Setup python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=frontend-builder /app/tmp/build/public/css /app/bart-dashboard/public/css

# Get the source code
COPY . /app/bart-dashboard
WORKDIR /app/bart-dashboard

CMD ["docker/entrypoint.sh", "flask", "run", "--with-threads"]

