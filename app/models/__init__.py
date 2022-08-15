from tortoise import Tortoise
from config.tortoise_config import AERICH_CONFIG


async def db_init():
    await Tortoise.init(config=AERICH_CONFIG)
    await Tortoise.generate_schemas()
