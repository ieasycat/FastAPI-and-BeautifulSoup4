from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config.config import CONFIG
from app.auth.apiexception import api_exception


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise api_exception(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise api_exception(status_code=403, detail="Invalid token.")
            return credentials.credentials
        else:
            raise api_exception(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = jwt.decode(jwtoken, CONFIG.JWT_SECRET_KEY, algorithms=CONFIG.JWT_ALGORITHM)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
