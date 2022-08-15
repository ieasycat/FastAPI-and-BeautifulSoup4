from fastapi import HTTPException
import json


def api_exception(status_code: int, detail: str) -> json:
    return HTTPException(
        status_code=status_code,
        detail=detail
        )
