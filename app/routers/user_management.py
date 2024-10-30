from typing import Annotated
from fastapi.params import Form

from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.models.organiser import Organiser
from app.models.user import User

import requests

user_management_router = APIRouter()
user_management_micro_service_path = "http://localhost:8000/"
@user_management_router.post("/user", tags=["user_management"],
    responses={
        200: {"description": "User creation successful"},
        400: {"description": "Corrupt user object passed"},
        500: {"description": "Database not live"},
        501: {"description": "Server not live"}
    }
)
async def create_user(user: User):
    try:
        # Forward the request data to the user creation endpoint
        response = requests.post(
            user_management_micro_service_path+"/user",
            headers={"Content-Type": "application/json"},
            json=user.dict() # Convert user data to JSON
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)

@user_management_router.put("/user", tags=["user_management"],
    responses={
        200: {"description": "User modification successful"},
        400: {"description": "Corrupt user object passed"},
        500: {"description": "Database not live"},
        501: {"description": "Server not live"},
    }
)
async def modify_user(user: User):
    try:
        # Forward the request data to the user creation endpoint
        response = requests.put(
            user_management_micro_service_path+"/user",
            headers={"Content-Type": "application/json"},
            json=user.dict() # Convert user data to JSON
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)

@user_management_router.delete(path="/user/{userId}", tags=["user_management"],
    responses={
        200: {"description": "User deletion successful"},
        400: {"description": "User not found"},
        500: {"description": "Database not live"},
        501: {"description": "Server not live"},
    }
)
async def delete_user(userId: str):
    try:
        # Forward the request data to the user creation endpoint
        response = requests.delete(
            user_management_micro_service_path + f"/user/{userId}",
            headers={"Content-Type": "application/json"},
            data=userId
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)

@user_management_router.get(path="/user/{userId}", tags=["user_management"],
    responses={
        200: {"description": "User fetched successfully"},
        400: {"description": "Corrupt user object passed"},
        500: {"description": "Database not live"},
        501: {"description": "Server not live"},
    }
)
async def get_user(userId: str):
    try:
        # Forward the request data to the user creation endpoint
        response = requests.get(
            user_management_micro_service_path + f"/user/{userId}",
            headers={"Content-Type": "application/json"},
            data=userId
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)

@user_management_router.post("/user/authenticate", tags=["user_management"],
    responses={
        200: {"description": "Authentication Successful"},
        401: {"description": "Unauthenticated - Incorrect Password"},
        404: {"description": "User not found"},
        501: {"description": "Server not live"},
        500: {"description": "Unexpected error"}
    }
)
async def authenticate_user(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    try:
        response = requests.post(
            user_management_micro_service_path+"/user/authenticate",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"email": email, "password": password}
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)


@user_management_router.post("/organiser", tags=["user_management"],
    responses={
        200: {"description": "Organiser creation successful"},
        400: {"description": "Corrupt organiser object passed"},
        500: {"description": "Database not live"},
        501: {"description": "Server not live"}
    }
)
async def create_organiser(organiser: Organiser):
    try:
        # Forward the request data to the user creation endpoint
        response = requests.post(
            user_management_micro_service_path+"/organiser",
            headers={"Content-Type": "application/json"},
            json=organiser.dict() # Convert user data to JSON
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)


@user_management_router.put("/organiser", tags=["user_management"],
    responses={
        200: {"description": "Organiser modification successful"},
        400: {"description": "Corrupt organiser object passed"},
        500: {"description": "Database not live"},
        501: {"description": "Server not live"}
    }
)
async def modify_organiser(organiser: Organiser):
    try:
        # Forward the request data to the user creation endpoint
        response = requests.put(
            user_management_micro_service_path+"/organiser",
            headers={"Content-Type": "application/json"},
            json=organiser.dict() # Convert user data to JSON
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)

@user_management_router.delete(path="/organiser/{organiserId}", tags=["user_management"],
    responses={
        200: {"description": "User deletion successful"},
        400: {"description": "User not found"},
        500: {"description": "Database not live"},
        501: {"description": "Server not live"},
    }
)
async def delete_user(organiserId: str):
    try:
        # Forward the request data to the user creation endpoint
        response = requests.delete(
            user_management_micro_service_path + f"/organiser/{organiserId}",
            headers={"Content-Type": "application/json"},
            data=organiserId
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)

@user_management_router.get(path="/organiser/{organiserId}", tags=["user_management"],
    responses={
        200: {"description": "Organiser fetched successfully"},
        400: {"description": "Corrupt Organiser object passed"},
        500: {"description": "Database not live"},
        501: {"description": "Server not live"},
    }
)
async def get_organiser(organiserId: str):
    try:
        # Forward the request data to the user creation endpoint
        response = requests.get(
            user_management_micro_service_path + f"/organiser/{organiserId}",
            headers={"Content-Type": "application/json"},
            data=organiserId
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)

@user_management_router.post("/organiser/authenticate", tags=["user_management"],
    responses={
        200: {"description": "Authentication Successful"},
        401: {"description": "Unauthenticated - Incorrect Password"},
        404: {"description": "Organiser not found"},
        501: {"description": "Server not live"},
        500: {"description": "Unexpected error"}
    }
)
async def authenticate_organiser(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    try:
        response = requests.post(
            user_management_micro_service_path+"/organiser/authenticate",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"email": email, "password": password}
        )
        status_code = response.status_code
        response = response.json()
        return JSONResponse(content=response, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={'status': 'connection failed', 'message': str(e)}, status_code=501)
