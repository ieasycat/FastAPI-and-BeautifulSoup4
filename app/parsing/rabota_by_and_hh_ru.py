from bs4 import BeautifulSoup
import httpx
from app.controller.dbcontroller import VacancyController
from app.models.apimodels import VacanciesAdd
from time import sleep
from app import logger


async def main():
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36'
    }

    technologies = ('Python', 'DevOps', 'Android', 'Flutter', 'UI UX')

    for technology in technologies:
        sleep(2)
        url = f'https://rabota.by/search/vacancy?search_field=name&text={technology}&items_on_page=20&search_period=1'

        try:
            req = httpx.get(url, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')

            pages = int(soup.find('div', class_='pager').find_all('a', class_='bloko-button')[-2].text) \
                if soup.find('div', class_='pager') else None

            vacancies_list = []

            if pages:
                for page in range(0, pages):
                    await parsing(
                        technology=technology,
                        page=page,
                        headers=headers,
                        vacancies_list=vacancies_list
                    )

            else:
                await parsing(
                    technology=technology,
                    page=0,
                    headers=headers,
                    vacancies_list=vacancies_list
                )
        except Exception as e:
            logger.error(msg=f'error: {e}', exc_info=True)
            pass


async def parsing(technology: str, page: int, headers: dict, vacancies_list: list):
    sleep(2)
    url_page = f'https://rabota.by/search/vacancy?search_field=name&text={technology}&items_on_page=20&' \
               f'search_period=1&page={page}'
    req_page = httpx.get(url=url_page, headers=headers)

    soup_page = BeautifulSoup(req_page.text, 'lxml')
    vacancies = soup_page.find_all('div', class_='serp-item')

    for vacancy in vacancies:
        url = vacancy.find('a', class_='bloko-link').get('href')
        description = vacancy.find('div', class_='g-user-content').find('div', class_='bloko-text').text if \
            vacancy.find('div', class_='g-user-content') else ''
        vacancies_list.append(
            VacanciesAdd(
                source=url.split('/')[2],
                technology='UI/UX' if technology == 'UI UX' else technology,
                description=description,
                url=url
            )
        )
    await VacancyController.add_vacancies(data=vacancies_list)
