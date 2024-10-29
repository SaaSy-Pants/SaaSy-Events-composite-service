from fastapi import APIRouter, HTTPException, Depends
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink
import httpx

router = APIRouter(prefix="/composite/users", tags=["composite_users"])

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()

@router.get("/{user_id}", response_model=HATEOASResponse)
async def get_composite_user(user_id: str, service: CompositeService = Depends(get_composite_service)):
    try:
        user = await service.get_user(user_id)
        links = [
            HATEOASLink(rel="self", href=f"/composite/users/{user_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/users/{user_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/users/{user_id}", method="DELETE"),
            HATEOASLink(rel="authenticate", href=f"/composite/users/authenticate", method="POST"),
        ]
        return HATEOASResponse(data=user, message="User retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/", response_model=HATEOASResponse)
async def create_composite_user(user_data: dict, service: CompositeService = Depends(get_composite_service)):
    try:
        result = await service.create_user(user_data)
        user_id = result.get("UID") or result.get("OID")
        links = [
            HATEOASLink(rel="self", href=f"/composite/users/{user_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/users/{user_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/users/{user_id}", method="DELETE"),
            HATEOASLink(rel="authenticate", href=f"/composite/users/authenticate", method="POST"),
        ]
        return HATEOASResponse(data=result, message="User created successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/authenticate", response_model=HATEOASResponse)
async def authenticate_composite_user(email: str, password: str, service: CompositeService = Depends(get_composite_service)):
    try:
        result = await service.authenticate_user(email, password)
        links = [
            HATEOASLink(rel="self", href=f"/composite/users/authenticate", method="POST"),
            HATEOASLink(rel="user_details", href=f"/composite/users/{result.get('UID')}", method="GET"),
        ]
        return HATEOASResponse(data=result, message="Authentication successful", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/{user_id}", response_model=HATEOASResponse)
async def modify_composite_user(user_id: str, user_data: dict, service: CompositeService = Depends(get_composite_service)):
    try:
        result = await service.modify_user(user_id, user_data)
        links = [
            HATEOASLink(rel="self", href=f"/composite/users/{user_id}", method="GET"),
            HATEOASLink(rel="delete", href=f"/composite/users/{user_id}", method="DELETE"),
            HATEOASLink(rel="authenticate", href=f"/composite/users/authenticate", method="POST"),
        ]
        return HATEOASResponse(data=result, message="User modified successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
