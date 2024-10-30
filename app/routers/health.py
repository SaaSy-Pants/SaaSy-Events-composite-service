from fastapi import APIRouter
from starlette.responses import JSONResponse
import requests

health_router = APIRouter()
user_management_micro_service_path = "http://localhost:8000/"
@health_router.get("/users", tags=["health"],
    responses={
        200: {"description": "Connection successful"},
        500: {"description": "Server not live"},
    })
async def health_check_users():
    response = None
    try:
        response = requests.get(user_management_micro_service_path + "/health/users")

        return response.json()

    except Exception as e:
        return JSONResponse(content = {'status': 'connection failed', 'message': str(e)}, status_code=500)

@health_router.get("/organisers", tags=["health"],
    responses={
        200: {"description": "Connection successful"},
        500: {"description": "Server not live"},
    })
async def health_check_organisers():
    response = None
    try:
        response = requests.get(user_management_micro_service_path + "/health/organisers")

        return response.json()

    except Exception as e:
        return JSONResponse(content = {'status': 'connection failed', 'message': str(e)}, status_code=500)