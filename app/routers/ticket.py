from fastapi import APIRouter, HTTPException, Depends, Response
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink
from app.utils.dependencies import get_token
import httpx

router = APIRouter(prefix="/composite/ticket", tags=["composite_ticket"])

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()

@router.post("/", response_model=HATEOASResponse)
async def book_ticket(booking_data: dict, service: CompositeService = Depends(get_composite_service), token: str = Depends(get_token), response: Response = None):
    try:
        result = await service.book_ticket(booking_data, token)
        booking_id = result.get("TID")

        eid = booking_data['eid']
        num_guests = booking_data['num_guests']

        event_details = await service.get_event(eid, token)
        old_guests_rem = event_details.get("GuestsRem")
        if old_guests_rem is None:
            raise HTTPException(status_code=500, detail="Unable to retrieve event details for guest update")

        new_guests_rem = old_guests_rem - num_guests
        if new_guests_rem < 0:
            raise HTTPException(status_code=400, detail="Not enough guests remaining for this event")

        await service.patch_event_guests(eid, new_guests_rem, token)

        links = [
            HATEOASLink(rel="self", href=f"/composite/event-booking/{booking_id}", method="GET"),
            HATEOASLink(rel="cancel", href=f"/composite/event-booking/{booking_id}", method="DELETE"),
            HATEOASLink(rel="book_again", href="/composite/event-booking", method="POST"),
        ]

        response.status_code = 201
        response.headers["Link"] = f"</composite/event-booking/{booking_id}>; rel=self"
        return HATEOASResponse(data=result, message="Event booking successful and guests updated", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{booking_id}", response_model=HATEOASResponse)
async def fetch_ticket(booking_id: str, service: CompositeService = Depends(get_composite_service), token: str = Depends(get_token)):
    try:
        booking = await service.fetch_ticket(booking_id, token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/event-booking/{booking_id}", method="GET"),
            HATEOASLink(rel="cancel", href=f"/composite/event-booking/{booking_id}", method="DELETE"),
            HATEOASLink(rel="book_new", href="/composite/event-booking", method="POST"),
        ]
        return HATEOASResponse(data=booking, message="Event booking details retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{booking_id}", response_model=HATEOASResponse)
async def cancel_ticket(booking_id: str, service: CompositeService = Depends(get_composite_service), token: str = Depends(get_token)):
    try:
        result = await service.cancel_ticket(booking_id, token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/event-booking/{booking_id}", method="DELETE"),
            HATEOASLink(rel="book_new", href="/composite/event-booking", method="POST"),
        ]
        return HATEOASResponse(data=result, message="Event booking canceled successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=HATEOASResponse)
async def get_tickets_of_user(user_id: str, service: CompositeService = Depends(get_composite_service), token: str = Depends(get_token)):
    try:
        tickets = await service.get_tickets_by_user(user_id, token)
        links = [
            HATEOASLink(rel="self", href=f"/composite/ticket/user/{user_id}", method="GET"),
            HATEOASLink(rel="with_events", href=f"/composite/ticket/user/{user_id}/all", method="GET"),
        ]
        return HATEOASResponse(data=tickets, message="Tickets retrieved successfully", links=links)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="User or tickets not found")
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/all", response_model=HATEOASResponse)
async def get_tickets_and_events_of_user(
    user_id: str,
    limit: int = 10,
    offset: int = 0,
    service: CompositeService = Depends(get_composite_service),
    token: str = Depends(get_token)
):
    try:
        combined_data = await service.get_tickets_and_events(user_id, limit=limit, offset=offset, token=token)
        
        current_limit = combined_data["events_pagination"]["limit"]
        current_offset = combined_data["events_pagination"]["offset"]
        has_next = combined_data["events_pagination"]["has_next"]
        has_prev = combined_data["events_pagination"]["has_prev"]

        links = [
            HATEOASLink(rel="self", href=f"/composite/ticket/user/{user_id}/all?limit={current_limit}&offset={current_offset}", method="GET"),
            HATEOASLink(rel="tickets_only", href=f"/composite/ticket/user/{user_id}", method="GET"),
        ]

        if has_next:
            next_offset = current_offset + current_limit
            links.append(
                HATEOASLink(
                    rel="next",
                    href=f"/composite/ticket/user/{user_id}/all?limit={current_limit}&offset={next_offset}",
                    method="GET"
                )
            )
        if has_prev:
            prev_offset = max(current_offset - current_limit, 0)
            links.append(
                HATEOASLink(
                    rel="prev",
                    href=f"/composite/ticket/user/{user_id}/all?limit={current_limit}&offset={prev_offset}",
                    method="GET"
                )
            )

        return HATEOASResponse(
            data=combined_data,
            message="Tickets and events retrieved successfully",
            links=links
        )
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="User or data not found")
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
