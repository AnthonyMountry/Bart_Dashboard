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

# Python Stage
FROM python:3.8.6-alpine3.12

RUN apk add --update \
    postgresql-dev \
    gcc \
    g++ \
    musl-dev \
    linux-headers \
    curl

# Install wait-for-it for docker-compose
# so that we can wait for the database to
# startup if we need to.
RUN curl -s https://raw.githubusercontent.com/eficode/wait-for/master/wait-for \
    -o /usr/local/bin/wait-for && \
  chmod +x /usr/local/bin/wait-for

# Setup python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install deps
RUN mkdir -p /app/build
COPY ./requirements.txt /app/build
WORKDIR /app/build

RUN pip install --upgrade pip wheel
RUN pip install -r requirements.txt

COPY --from=frontend-builder /app/tmp/build/public/css /app/bart-dashboard/public/css

# COPY ./db/bart_data.zip /app/tmp/data
# WORKDIR /app/tmp/data
# RUN unzip bart_data.zip

# Get the source code
COPY . /app/bart-dashboard
WORKDIR /app/bart-dashboard

CMD ["docker/entrypoint.sh", "flask", "run", "--with-threads"]

