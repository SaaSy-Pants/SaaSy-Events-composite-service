from fastapi import APIRouter, HTTPException, Depends
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink
from app.utils.dependencies import get_token, verify_custom_jwt

router = APIRouter(prefix="/composite/organizer", tags=["composite_organizer"])

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()

@router.get("/{organizer_id}", response_model=HATEOASResponse)
async def get_organizer(
    organizer_id: str,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    
    verify_custom_jwt(token, "organizer")  # Validate JWT with 'organizer' role
    try:
        organizer = await service.get_organizer(organizer_id, token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/organizer/{organizer_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/organizer/{organizer_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/organizer/{organizer_id}", method="DELETE"),
        ]
        return HATEOASResponse(data=organizer, message="Organizer retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("message", "Error retrieving organizer")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=HATEOASResponse, status_code=201)
async def create_organizer(
    organizer_data: dict,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):

    verify_custom_jwt(token, "organizer")  # Validate JWT with 'organizer' role
    try:
        organizer = await service.create_organizer(organizer_data, token)
        organizer_id = organizer.get("organizer_id")
        links = [
            HATEOASLink(rel="self", href=f"/composite/organizer/{organizer_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/organizer/{organizer_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/organizer/{organizer_id}", method="DELETE"),
        ]
        return HATEOASResponse(data=organizer, message="Organizer created successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("message", "Error creating organizer")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{organizer_id}", response_model=HATEOASResponse)
async def update_organizer(
    organizer_id: str,
    organizer_data: dict,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
  
    verify_custom_jwt(token, "organizer")  # Validate JWT with 'organizer' role
    try:
        organizer = await service.update_organizer(organizer_id, organizer_data, token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/organizer/{organizer_id}", method="GET"),
            HATEOASLink(rel="delete", href=f"/composite/organizer/{organizer_id}", method="DELETE"),
        ]
        return HATEOASResponse(data=organizer, message="Organizer updated successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("message", "Error updating organizer")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{organizer_id}", response_model=HATEOASResponse)
async def delete_organizer(
    organizer_id: str,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):

    verify_custom_jwt(token, "organizer")  # Validate JWT with 'organizer' role
    try:
        await service.delete_organizer(organizer_id, token)
        links = [
            HATEOASLink(rel="create", href="/composite/organizer", method="POST"),
        ]
        return HATEOASResponse(message="Organizer deleted successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json().get("message", "Error deleting organizer")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
