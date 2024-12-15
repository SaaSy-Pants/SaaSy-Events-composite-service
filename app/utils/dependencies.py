import os

import jwt
from fastapi import Request, HTTPException
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError


def get_token(request: Request) -> str:
    return extract_access_token_from_header(request)

def extract_access_token_from_header(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header is missing or invalid")

    return auth_header.split(" ")[1]

def verify_custom_jwt(token, profile):
    try:
        decoded_token = jwt.decode(
            token,
            key=os.getenv('JWT_SECRET_KEY'),
            algorithms=['HS256']
        )
        if decoded_token.get('profile') != profile:
            raise HTTPException(status_code=403, detail="Access denied.")

        return decoded_token

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The auth token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="The auth token is invalid")
