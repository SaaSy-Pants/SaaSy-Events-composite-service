import httpx
from fastapi import APIRouter, HTTPException, Depends
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink
from app.utils.dependencies import get_token, verify_custom_jwt

router = APIRouter(prefix="/composite/organiser", tags=["composite_organiser"])

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()

@router.get("/{organiser_id}", response_model=HATEOASResponse)
async def get_organiser(
    organiser_id: str,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    
    verify_custom_jwt(token, "user")  # Validate JWT with 'organiser' role
    try:
        organiser = await service.get_organiser(organiser_id, token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/organiser/{organiser_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/organiser/{organiser_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/organiser/{organiser_id}", method="DELETE"),
        ]
        return HATEOASResponse(data=organiser, message="organiser retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("message", "Error retrieving organiser")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=HATEOASResponse, status_code=201)
async def create_organiser(
    organiser_data: dict,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):

    verify_custom_jwt(token, "organiser")  # Validate JWT with 'organiser' role
    try:
        organiser = await service.create_organiser(organiser_data, token)
        organiser_id = organiser.get("organiser_id")
        links = [
            HATEOASLink(rel="self", href=f"/composite/organiser/{organiser_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/organiser/{organiser_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/organiser/{organiser_id}", method="DELETE"),
        ]
        return HATEOASResponse(data=organiser, message="organiser created successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("message", "Error creating organiser")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{organiser_id}", response_model=HATEOASResponse)
async def update_organiser(
    organiser_id: str,
    organiser_data: dict,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
  
    verify_custom_jwt(token, "organiser")  # Validate JWT with 'organiser' role
    try:
        organiser = await service.update_organiser(organiser_id, organiser_data, token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/organiser/{organiser_id}", method="GET"),
            HATEOASLink(rel="delete", href=f"/composite/organiser/{organiser_id}", method="DELETE"),
        ]
        return HATEOASResponse(data=organiser, message="organiser updated successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("message", "Error updating organiser")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{organiser_id}", response_model=HATEOASResponse)
async def delete_organiser(
    organiser_id: str,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):

    verify_custom_jwt(token, "organiser")  # Validate JWT with 'organiser' role
    try:
        await service.delete_organiser(organiser_id, token)
        links = [
            HATEOASLink(rel="create", href="/composite/organiser", method="POST"),
        ]
        return HATEOASResponse(message="organiser deleted successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("message", "Error deleting organiser")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=HATEOASResponse)
async def get_organiser(service: CompositeService = Depends(get_composite_service), token: str = Depends(get_token)):
    organiser_info = verify_custom_jwt(token, 'organiser')
    email = organiser_info.get('email')
    if not email:
        raise HTTPException(status_code=400, detail="Email not found in token")

    try:
        user = await service.get_organiser_by_email(email, token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/organiser", method="GET"),
        ]
        return HATEOASResponse(data=user, message="Organiser retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("message", "Error fetching organiser")
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")