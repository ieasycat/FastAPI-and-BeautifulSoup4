# Vacancy-manager

A module, which parses popular recruiting platforms, recording everything in the database. The parser is launched automatically, and is performed every 30 minutes, as well as cleaning of outdated data in the database is provided. This application is asynchronous. The code is covered with tests. It is also ready for deployment on Heroku and containerized for Docker.

Stack: FastAPI, BeautifulSoup4, Celery, Redis, Tortoise, PostgresSQL, PyTest

command for docker: docker-compose up -d --build
