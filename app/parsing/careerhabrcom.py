import httpx
from bs4 import BeautifulSoup
from datetime import date
from app.models.apimodels import VacanciesAdd
from app.controller.dbcontroller import VacancyController
from time import sleep
from app import logger


async def parsing(soup: BeautifulSoup, technology: str, data: list) -> list:
    vacancies = soup.find_all('div', class_="vacancy-card__inner")
    day_now = date.today().strftime("%Y-%m-%d")
    for vacancy in vacancies:
        vacancy_date = vacancy.find('time', class_="basic-date").get('datetime').split('T')[0]
        if vacancy_date == day_now:
            description = vacancy.find('div', class_="vacancy-card__skills").text \
                if vacancy.find('div', class_="vacancy-card__skills").text else ' '
            vacancy_name = vacancy.find('div', class_="vacancy-card__title").text.lower()
            technology = 'UI/UX' if technology == 'Ui%2FUX' else technology
            if technology.lower() in vacancy_name:
                url = 'https://career.habr.com' + vacancy.find('a', class_="vacancy-card__icon-link").get('href')
                vacancy_data = VacanciesAdd(source="career.habr.com",
                                            technology=technology,
                                            description=description,
                                            url=url)
                data.append(vacancy_data)

    check_pagination = soup.find('div', class_="paginator")
    data = await paginator(pagination=check_pagination, data=data, technology=technology)
    return data


async def paginator(pagination: BeautifulSoup, data: list, technology: str) -> list:
    if pagination and pagination.find('a', class_='page next'):
        sleep(0.1)
        url_page = "https://career.habr.com" + pagination.find('a', class_="page next").get('href')
        request_page = httpx.get(url=url_page)
        soup_page = BeautifulSoup(request_page.text, 'lxml')
        await parsing(soup=soup_page, data=data, technology=technology)
    return data


async def main():
    technologies = ('Python', 'Android', 'Ui%2FUX', 'DevOps', "Flutter")
    for technology in technologies:
        url = f'https://career.habr.com/vacancies?q={technology}' \
              f'&s[]=2&s[]=3&s[]=82&s[]=5&s[]=22&s[]=23&sort=date&type=all'
        try:
            request_vacancies = httpx.get(url=url)
            soup = BeautifulSoup(request_vacancies.text, 'lxml')
            vacancies_list = await parsing(soup, technology, data=[])
            if vacancies_list:
                await VacancyController.add_vacancies(data=vacancies_list)
        except Exception as e:
            logger.error(msg=f'error: {e}', exc_info=True)
            pass
