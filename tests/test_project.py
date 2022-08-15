import datetime
import pytest
from app.models.db import Vacancy, Source
from app.parsing import rabota_by_and_hh_ru, careerhabrcom, jobsdevbyio
from app.scripts import __all__


@pytest.mark.anyio
async def test_vacancies(client, add_vacancy):
    response = await client.get("/api/v1/pd/vacancy/")
    assert response.status_code == 200
    assert len(response.json()['vacancies']) == 3


@pytest.mark.anyio
async def test_vacancies_filter(client, add_vacancy):
    response = await client.get("/api/v1/pd/vacancy/filter/", params="text=technology")
    assert response.status_code == 200
    assert len(response.json()['vacancies']) == 1
    assert response.json()['vacancies'][0]['id'] == 1
    assert response.json()['vacancies'][0]['technology'] == 'technology'
    assert response.json()['vacancies'][0]['source'] == 'testsource'
    assert response.json()['vacancies'][0]['description'] == 'description'
    assert response.json()['vacancies'][0]['url'] == 'url'
    assert response.json()['vacancies'][0]['date'] == datetime.datetime.now().strftime('%d-%m-%Y')


@pytest.mark.anyio
async def test_db_str(client):
    vac = await Vacancy.filter(id=1).first()
    source = await Source.filter(id=1).first()
    assert vac.__str__() == 'technology'
    assert source.__str__() == 'testsource'


@pytest.mark.anyio
async def test_parsing(client, add_source):
    await rabota_by_and_hh_ru.main()
    await careerhabrcom.main()
    await jobsdevbyio.main()
    response = await client.get("/api/v1/pd/vacancy/")
    assert 'hh.ru' or 'rabota.by' in response.text
    assert 'career.habr.com' in response.text
    assert 'jobs.devby.io' in response.text


def test_scripts_init(client):
    assert len(__all__) == 1
