from fastapi import APIRouter, HTTPException, Depends
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink

user_router = APIRouter()

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()

@user_router.post("/", response_model=HATEOASResponse, status_code=201)
async def create_user(user_data: dict, service: CompositeService = Depends(get_composite_service)):
    try:
        result = await service.create_user(user_data)
        user_id = result.get("UID")
        links = [
            HATEOASLink(rel="self", href=f"/composite/user/{user_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/user/{user_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/user/{user_id}", method="DELETE"),
        ]
        return HATEOASResponse(data=result, message="User created successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json().get("message", "Error creating user"))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user_router.get("/{user_id}", response_model=HATEOASResponse)
async def get_user(user_id: str, service: CompositeService = Depends(get_composite_service)):
    try:
        user = await service.get_user(user_id)
        links = [
            HATEOASLink(rel="self", href=f"/composite/user/{user_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/user/{user_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/user/{user_id}", method="DELETE"),
        ]
        return HATEOASResponse(data=user, message="User retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user_router.put("/", response_model=HATEOASResponse)
async def modify_user(user_data: dict, service: CompositeService = Depends(get_composite_service)):
    try:
        result = await service.modify_user(user_data)
        user_id = result.get("UID")
        links = [
            HATEOASLink(rel="self", href=f"/composite/user/{user_id}", method="GET"),
            HATEOASLink(rel="delete", href=f"/composite/user/{user_id}", method="DELETE"),
        ]
        return HATEOASResponse(data=result, message="User updated successfully", links=links)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 400:
            raise HTTPException(status_code=400, detail="Bad Request: Invalid user data")
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user_router.delete("/{user_id}", response_model=HATEOASResponse)
async def delete_user(user_id: str, service: CompositeService = Depends(get_composite_service)):
    try:
        result = await service.delete_user(user_id)
        links = [
            HATEOASLink(rel="create", href="/composite/user", method="POST"),
        ]
        return HATEOASResponse(data=result, message="User deleted successfully", links=links)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 400:
            raise HTTPException(status_code=400, detail="Bad Request: User not found")
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
