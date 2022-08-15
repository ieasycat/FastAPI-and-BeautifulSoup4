from pydantic import BaseSettings
from config.config import CONFIG


class TortoiseSettings(BaseSettings):
    db_models = ['app.models.db', 'app.auth.models.userdb', 'aerich.models']

    @property
    def tortoise_config(self):
        return {
            "connections": {"default":  CONFIG.DATABASE_URL},
            "apps": {
                "models": {
                    "models": self.db_models,
                    "default_connection": "default",
                }
            },
        }


tortoise_settings = TortoiseSettings()
AERICH_CONFIG = tortoise_settings.tortoise_config
