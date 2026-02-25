FROM python:3.14.0

RUN apt-get update -y

RUN pip install --upgrade pip

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

RUN playwright install firefox
RUN playwright install-deps firefox

RUN playwright install chromium
RUN playwright install-deps chromium

COPY . /app