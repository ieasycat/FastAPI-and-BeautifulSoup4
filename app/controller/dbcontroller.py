from tortoise.expressions import Q
from app.models.db import Vacancy, Source
from datetime import timedelta, datetime


class VacancyController:

    @staticmethod
    async def get_all_vacancies() -> list:
        return await Vacancy.all().prefetch_related('source').order_by("-date")

    @classmethod
    async def add_vacancies(cls, data: list):
        for el in data:
            if not await cls.check_url(el.url):
                await Vacancy.create(source_id=await SourceController.get_source_id(el.source),
                                     technology=el.technology,
                                     description=el.description,
                                     url=el.url)

    @staticmethod
    async def delete():
        delete_after = datetime.today() - timedelta(days=15)
        vacancies_to_delete = await Vacancy.filter(date__lte=delete_after)
        for el in vacancies_to_delete:
            await Vacancy.filter(id=el.id).delete()

    @staticmethod
    async def check_url(url: str) -> list | None:
        return await Vacancy.filter(url=url)

    @staticmethod
    async def filter(text) -> list:
        vacancies = await Vacancy.filter(
            Q(Q(technology=text), Q(source__name=text), join_type='OR')).prefetch_related('source').order_by("-date")
        return vacancies


class SourceController:

    @staticmethod
    async def get_source_id(source_name: str) -> int:
        source = await Source.get_or_none(name=source_name)
        if not source:
            source = await Source.create(name=source_name)
        return source.id

    @staticmethod
    async def add_source(source: str):
        return await Source.create(name=source)
