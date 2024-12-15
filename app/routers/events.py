from fastapi import APIRouter, HTTPException, Depends, Query, Response, BackgroundTasks
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink
from app.utils.dependencies import get_token, verify_custom_jwt
import httpx

router = APIRouter(prefix="/composite/events", tags=["composite_events"])

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()

def validate_token(token: str):
    try:
        try:
            return verify_custom_jwt(token, 'user')
        except HTTPException:
            return verify_custom_jwt(token, 'organiser')
    except HTTPException:
        raise HTTPException(status_code=403, detail="Access denied: Unauthorized role")

@router.get("/{event_id}", response_model=HATEOASResponse)
async def get_composite_event(event_id: str, service: CompositeService = Depends(get_composite_service), token: str = Depends(get_token)):
    validate_token(token)
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

@router.get("", response_model=HATEOASResponse)
async def get_all_composite_events(
    limit: int = Query(10, ge=1),
    offset: int = Query(1, ge=1, le=100),
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    validate_token(token)
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
    background_tasks: BackgroundTasks,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token),
    response: Response = None,
    async_create: bool = Query(False, description="If true, returns 202 Accepted for async pattern.")
):
    validate_token(token)
    try:
        if async_create:
            background_tasks.add_task(process_event_creation, event_data, token, service)
            response.status_code = 202
            response.headers["Location"] = f"/composite/events/status/{event_data.get('EID', 'pending')}"
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

async def process_event_creation(event_data: dict, token: str, service: CompositeService):
    try:
        result = await service.create_event(event_data, token)
        print("Event created in background:", result)
    except Exception as e:
        print(f"Error during event creation in background: {e}")

@router.put("", response_model=HATEOASResponse)
async def update_composite_event(
    event_data: dict, 
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    validate_token(token)
    try:
        result = await service.update_event(event_data, token)
        event_id = result.get("EID")
        links = [
            HATEOASLink(rel="self", href=f"/composite/events/{event_id}", method="GET"),
            HATEOASLink(rel="delete", href=f"/composite/events/{event_id}", method="DELETE"),
            HATEOASLink(rel="tickets", href=f"/composite/events/{event_id}/tickets", method="GET"),
        ]
        user_ids = await service.get_users_by_event(event_id, 100, 0, token)
        user_emails = []
        for attendee in user_ids['uids']:
            profile = await service.get_user(attendee['UID'], token)
            user_emails.append(profile['details']['Email'])

        if len(user_emails) > 0:
            event_data['UserEmails'] = list(set(user_emails))
            await service.publish_event_update_notification(event_data)
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
    validate_token(token)
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

@router.get("/organiser/{oid}", response_model=HATEOASResponse)
async def get_events_by_organizer(
    oid: str,
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    validate_token(token)
    try:
        events = await service.get_events_by_organizer(oid, limit=limit, offset=offset, token=token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/events/organiser/{oid}?limit={limit}&offset={offset}", method="GET"),
        ]
        return HATEOASResponse(data=events, message="Events retrieved successfully", links=links)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch events: {str(e)}")


@router.patch("/{eid}/{guests_remaining}", response_model=HATEOASResponse)
async def update_guests_remaining(
    eid: str,
    guests_remaining: int,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    validate_token(token)
    try:
        success = await service.update_guests_remaining(eid, guests_remaining, token)
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")

        links = [
            HATEOASLink(rel="self", href=f"/composite/events/{eid}/guests_remaining", method="PATCH"),
            HATEOASLink(rel="event_details", href=f"/composite/events/{eid}", method="GET"),
        ]
        return HATEOASResponse(data={"eid": eid, "guests_remaining": guests_remaining},
                               message="Guests remaining updated successfully", links=links)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
