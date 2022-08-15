import httpx
from bs4 import BeautifulSoup
from app.controller.dbcontroller import VacancyController
from app.models.apimodels import VacanciesAdd
from time import sleep
from app import logger


async def main():
    technologies = ('Python', 'Android', 'DevOps/Sysadmin', 'UX/Design')
    vacancies_list = []
    for technology in technologies:
        url = f'https://jobs.devby.io/?filter[specialization_title]={technology}'

        try:
            request_vacancies = httpx.get(url=url)
            soup = BeautifulSoup(request_vacancies.text, 'lxml')
            technology = 'DevOps' if technology == 'DevOps/Sysadmin' else technology
            technology = 'UI/UX' if technology == 'UX/Design' else technology
            vacancies = soup.find_all('div', class_="vacancies-list-item__body js-vacancies-list-item--open")

            await parser(vacancies_list=vacancies_list, vacancies=vacancies, technology=technology)
        except Exception as e:
            logger.error(msg=f'error: {e}', exc_info=True)
            pass


async def parser(vacancies_list: list, vacancies: list, technology: str):
    for vacancy in vacancies:
        sleep(0.5)
        url = 'https://jobs.devby.io' + vacancy.find('div', class_="vacancies-list-item__position"). \
            find('a', class_="vacancies-list-item__link_block").get('href')

        vacancy_data = VacanciesAdd(source="jobs.devby.io",
                                    technology=technology,
                                    description=await get_description(url=url),
                                    url=url)
        vacancies_list.append(vacancy_data)
    await VacancyController.add_vacancies(data=vacancies_list)


async def get_description(url: str) -> str:
    request_description = httpx.get(url=url)
    description_soup = BeautifulSoup(request_description.text, 'lxml')
    description_elements = description_soup.find_all('div', class_="vacancy__info-block__item")
    description = ''
    if description_elements:
        for el in description_elements:
            description += el.text + " "
    return description
