web: aerich upgrade; gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
worker: celery -A app.scripts worker --beat -s celerybeat-scedule --loglevel INFO