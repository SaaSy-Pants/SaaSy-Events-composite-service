from fastapi import APIRouter, HTTPException, Depends, Query, Response
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink
from app.utils.dependencies import get_token
import httpx

router = APIRouter(prefix="/composite/events", tags=["composite_events"])

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()

@router.get("/{event_id}", response_model=HATEOASResponse)
async def get_composite_event(event_id: str, service: CompositeService = Depends(get_composite_service), token: str = Depends(get_token)):
    try:
        event = await service.get_event(event_id, token)
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
    limit: int = Query(1, ge=1),
    offset: int = Query(10, ge=1, le=100),
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    try:
        events = await service.get_all_events(limit=limit, offset=offset, token=token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/events?limit={limit}&offset={offset}", method="GET"),
            HATEOASLink(rel="create", href="/composite/events", method="POST"),
        ]
        return HATEOASResponse(data=events, message="Events retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=HATEOASResponse)
async def create_composite_event(
    event_data: dict, 
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token),
    response: Response = None,
    async_create: bool = Query(False, description="If true, returns 202 Accepted for async pattern.")
):
    try:
        if async_create:
            response.status_code = 202
            response.headers["Location"] = f"/composite/events/status/{event_data.get('EID','pending')}"
            return HATEOASResponse(data={}, message="Event creation accepted, processing asynchronously", links=[])
        else:
            result = await service.create_event(event_data, token)
            event_id = result.get("EID")
            links = [
                HATEOASLink(rel="self", href=f"/composite/events/{event_id}", method="GET"),
                HATEOASLink(rel="modify", href=f"/composite/events/{event_id}", method="PUT"),
                HATEOASLink(rel="delete", href=f"/composite/events/{event_id}", method="DELETE"),
                HATEOASLink(rel="tickets", href=f"/composite/events/{event_id}/tickets", method="GET"),
            ]
            response.status_code = 201
            response.headers["Link"] = f"</composite/events/{event_id}>; rel=self"
            return HATEOASResponse(data=result, message="Event created successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("", response_model=HATEOASResponse)
async def update_composite_event(
    event_data: dict, 
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    try:
        result = await service.update_event(event_data, token)
        event_id = result.get("EID")
        links = [
            HATEOASLink(rel="self", href=f"/composite/events/{event_id}", method="GET"),
            HATEOASLink(rel="delete", href=f"/composite/events/{event_id}", method="DELETE"),
            HATEOASLink(rel="tickets", href=f"/composite/events/{event_id}/tickets", method="GET"),
        ]
        return HATEOASResponse(data=result, message="Event updated successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{event_id}", response_model=HATEOASResponse)
async def delete_composite_event(
    event_id: str, 
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    try:
        await service.delete_event(event_id, token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/events/{event_id}", method="DELETE"),
            HATEOASLink(rel="create", href="/composite/events", method="POST"),
        ]
        return HATEOASResponse(message="Event deleted successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
