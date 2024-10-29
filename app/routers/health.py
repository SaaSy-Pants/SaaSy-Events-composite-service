
from fastapi import APIRouter, HTTPException, Depends
from app.services.composite_service import CompositeService
from app.models.response import HATEOASResponse, HATEOASLink
import httpx

router = APIRouter(prefix="/composite/health", tags=["composite_health"])

async def get_composite_service():
    service = CompositeService()
    try:
        yield service
    finally:
        await service.close()

@router.get("/", response_model=HATEOASResponse)
async def composite_health_check(service: CompositeService = Depends(get_composite_service)):
    try:
        #Checking User Management Health
        user_health = await service.client.get(f"{service.config.USER_MGMT_URL}/health")
        user_health.raise_for_status()
        user_health_status = user_health.json()

        #Checking Event Management Health
        event_health = await service.client.get(f"{service.config.EVENT_MGMT_URL}/health")
        event_health.raise_for_status()
        event_health_status = event_health.json()

        #Checking Event Booking Health
        event_booking_health = await service.client.get(f"{service.config.TICKET_URL}/health")
        event_booking_health.raise_for_status()
        event_booking_health_status = event_booking_health.json()

        combined_health = {
            "user_management": user_health_status,
            "event_management": event_health_status,
            "event_booking": event_booking_health_status
        }

        links = [
            HATEOASLink(rel="self", href="/composite/health", method="GET"),
            HATEOASLink(rel="users", href="/composite/users", method="GET"),
            HATEOASLink(rel="events", href="/composite/events", method="GET"),
            HATEOASLink(rel="event_booking", href="/composite/event-booking", method="GET"),
        ]

        return HATEOASResponse(data=combined_health, message="All services are healthy", links=links)
    except httpx.HTTPStatusError as exc:
        links = [
            HATEOASLink(rel="self", href="/composite/health", method="GET"),
        ]
        return HATEOASResponse(
            data={"status": "error", "details": exc.response.text},
            message="One or more services are unhealthy",
            links=links
        )
    except Exception as e:
        links = [
            HATEOASLink(rel="self", href="/composite/health", method="GET"),
        ]
        return HATEOASResponse(
            data={"status": "error", "details": str(e)},
            message="An unexpected error occurred",
            links=links
        )
