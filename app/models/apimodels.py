from typing import List
from fastapi import Query
from pydantic import BaseModel


class VacanciesResponse(BaseModel):
    id: int
    source: str
    date: str
    technology: str
    description: str
    url: str


class VacanciesAdd(BaseModel):
    source: str
    technology: str
    description: str
    url: str


class AllVacanciesResponse(BaseModel):
    vacancies: List[VacanciesResponse]


class QueryParams:
    def __init__(
            self,
            text: str = Query(..., description="Source or vacancy"),
                ):
        self.text = text
