
from fastapi import APIRouter, HTTPException, Depends, Query
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink
import httpx

router = APIRouter(prefix="/composite/events", tags=["composite_events"])

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()


@router.get("/{event_id}", response_model=HATEOASResponse)
async def get_composite_event(event_id: str, service: CompositeService = Depends(get_composite_service)):
    try:
        event = await service.get_event(event_id)
        links = [
            HATEOASLink(rel="self", href=f"/composite/events/{event_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/events/{event_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/events/{event_id}", method="DELETE"),
            HATEOASLink(rel="tickets", href=f"/composite/events/{event_id}/tickets", method="GET"),
        ]
        return HATEOASResponse(data=event, message="Event retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/", response_model=HATEOASResponse)
async def get_all_composite_events(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    service: CompositeService = Depends(get_composite_service)
):
    try:
        events = await service.get_all_events(page=page, size=size)
        links = [
            HATEOASLink(rel="self", href=f"/composite/events?page={page}&size={size}", method="GET"),
            HATEOASLink(rel="create", href="/composite/events", method="POST"),
        ]
        return HATEOASResponse(data=events, message="Events retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=HATEOASResponse)
async def create_composite_event(event_data: dict, service: CompositeService = Depends(get_composite_service)):
    try:
        result = await service.create_event(event_data)
        event_id = result.get("EID")
        links = [
            HATEOASLink(rel="self", href=f"/composite/events/{event_id}", method="GET"),
            HATEOASLink(rel="modify", href=f"/composite/events/{event_id}", method="PUT"),
            HATEOASLink(rel="delete", href=f"/composite/events/{event_id}", method="DELETE"),
            HATEOASLink(rel="tickets", href=f"/composite/events/{event_id}/tickets", method="GET"),  # Example
        ]
        return HATEOASResponse(data=result, message="Event created successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/{event_id}", response_model=HATEOASResponse)
async def update_composite_event(event_id: str, event_data: dict, service: CompositeService = Depends(get_composite_service)):
    try:
        result = await service.update_event(event_id, event_data)
        links = [
            HATEOASLink(rel="self", href=f"/composite/events/{event_id}", method="GET"),
            HATEOASLink(rel="delete", href=f"/composite/events/{event_id}", method="DELETE"),
            HATEOASLink(rel="tickets", href=f"/composite/events/{event_id}/tickets", method="GET"),  # Example
        ]
        return HATEOASResponse(data=result, message="Event updated successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/{event_id}", response_model=HATEOASResponse)
async def delete_composite_event(event_id: str, service: CompositeService = Depends(get_composite_service)):
    try:
        await service.delete_event(event_id)
        links = [
            HATEOASLink(rel="self", href=f"/composite/events/{event_id}", method="DELETE"),
            HATEOASLink(rel="create", href="/composite/events", method="POST"),
        ]
        return HATEOASResponse(message="Event deleted successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
