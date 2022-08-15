from datetime import timedelta, datetime
import pytest
from httpx import AsyncClient
from tortoise import Tortoise
from app import app
from app.controller.dbcontroller import VacancyController
from app.models.apimodels import VacanciesAdd
from app.models.db import Source, Vacancy

DB_URL = "sqlite://:memory:"


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": ['app.models.db', 'app.auth.models.userdb', 'aerich.models']}, _create_db=create_db
    )
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = DB_URL):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="session")
async def add_vacancy(add_source):
    data = [
        VacanciesAdd(source="testsource", technology="technology", description="description", url="url"),
        VacanciesAdd(source="testsource", technology="python", description="description", url="urltest"),
    ]
    await VacancyController.add_vacancies(data)
    await Vacancy.create(source_id=1, technology="DevOps", description="description", url="urltest",
                         date=datetime.today() - timedelta(days=15))
