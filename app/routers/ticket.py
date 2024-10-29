
from fastapi import APIRouter, HTTPException, Depends
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink
import httpx

router = APIRouter(prefix="/composite/ticket", tags=["composite_ticket"])

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()


@router.post("/", response_model=HATEOASResponse)
async def book_ticket(booking_data: dict, service: CompositeService = Depends(get_composite_service)):
    
    try:
        result = await service.book_ticket(booking_data)
        booking_id = result.get("TID")
        links = [
            HATEOASLink(rel="self", href=f"/composite/event-booking/{booking_id}", method="GET"),
            HATEOASLink(rel="cancel", href=f"/composite/event-booking/{booking_id}", method="DELETE"),
            HATEOASLink(rel="book_again", href="/composite/event-booking", method="POST"),
        ]
        return HATEOASResponse(data=result, message="Event booking successful", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{booking_id}", response_model=HATEOASResponse)
async def fetch_ticket(booking_id: str, service: CompositeService = Depends(get_composite_service)):
  
    try:
        booking = await service.fetch_ticket(booking_id)
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
async def cancel_ticket(booking_id: str, service: CompositeService = Depends(get_composite_service)):
    
    try:
        result = await service.cancel_ticket(booking_id)
        links = [
            HATEOASLink(rel="self", href=f"/composite/event-booking/{booking_id}", method="DELETE"),
            HATEOASLink(rel="book_new", href="/composite/event-booking", method="POST"),
        ]
        return HATEOASResponse(data=result, message="Event booking canceled successfully", links=links)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
