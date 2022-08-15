from celery import Celery
from config.config import CONFIG
from celery.schedules import crontab
from app.parsing import rabota_by_and_hh_ru, jobsdevbyio, careerhabrcom
from app.models import db_init
from tortoise import run_async
from app.controller.dbcontroller import VacancyController
from app import logger

'''
celery -A app.scripts worker --beat -s celerybeat-scedule --loglevel INFO
'''

celery_app = Celery(__name__)
celery_app.conf.broker_url = CONFIG.REDIS_URL


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, *args, **kwargs):
    sender.add_periodic_task(crontab(minute='*/30'), parsing.s())
    sender.add_periodic_task(crontab(minute=0, hour=0), delete.s())


@celery_app.task
def parsing():
    run_async(db_init())
    logger.info(msg='Start parsing')
    run_async(jobsdevbyio.main())
    run_async(careerhabrcom.main())
    run_async(rabota_by_and_hh_ru.main())
    logger.info(msg='Finish parsing')


@celery_app.task
def delete():
    logger.info(msg='Start delete')
    run_async(VacancyController.delete())
    logger.info(msg='Finish delete')
