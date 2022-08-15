from logging.handlers import RotatingFileHandler
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.auth.controller.jwt_bearer import JWTBearer
from config.tortoise_config import AERICH_CONFIG
from app.views.apiview import router
from app.auth.views.authview import auth_router
import logging
import os
from fastapi import Depends


app = FastAPI()

app.include_router(router=router, prefix='/api/v1/pd/vacancy', dependencies=[Depends(JWTBearer())], tags=["API"])
app.include_router(router=auth_router, prefix='/auth', tags=["Authorize"])

register_tortoise(app, config=AERICH_CONFIG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/vacancies_manager.log', maxBytes=20480,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)
    logger.info('Vacancies manager startup')
