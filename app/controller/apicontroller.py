from app.controller.dbcontroller import VacancyController
from app.models.apimodels import VacanciesResponse, AllVacanciesResponse


class ApiControllerVacancy:

    @staticmethod
    async def get_all_vacancies() -> AllVacanciesResponse:
        vacancies_list = await VacancyController.get_all_vacancies()
        return AllVacanciesResponse(vacancies=[VacanciesResponse(id=el.id,
                                                                 source=el.source.name,
                                                                 date=el.date.strftime('%d-%m-%Y'),
                                                                 technology=el.technology,
                                                                 description=el.description,
                                                                 url=el.url) for el in vacancies_list])

    @staticmethod
    async def filter(text: str) -> AllVacanciesResponse:
        vacancies_list = await VacancyController.filter(text)
        return AllVacanciesResponse(vacancies=[VacanciesResponse(id=el.id,
                                                                 source=el.source.name,
                                                                 date=el.date.strftime('%d-%m-%Y'),
                                                                 technology=el.technology,
                                                                 description=el.description,
                                                                 url=el.url) for el in vacancies_list])
