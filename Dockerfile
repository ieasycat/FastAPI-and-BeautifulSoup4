FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /vacancies_manager

COPY requirements.txt /vacancies_manager
COPY boot.sh .

RUN pip3 install --upgrade pip -r requirements.txt
RUN chmod +x boot.sh

COPY ./ .

RUN chmod +x /vacancies_manager/boot.sh






