from fastapi import APIRouter
from app.controller.apicontroller import ApiControllerVacancy
from app.models.apimodels import AllVacanciesResponse, QueryParams
from fastapi import Depends


router = APIRouter()


@router.get('/', response_model=AllVacanciesResponse)
async def get_vacancies():
    return await ApiControllerVacancy.get_all_vacancies()


@router.get('/filter/', response_model=AllVacanciesResponse)
async def filters(text, params: QueryParams = Depends()):
    return await ApiControllerVacancy.filter(text)
