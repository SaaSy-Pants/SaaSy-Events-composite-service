import httpx
from app.utils.config import Config
import asyncio

config = Config()

class CompositeService:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.config = Config()

    async def close(self):
        await self.client.aclose()

    def _get_headers(self, token: str):
        return {"Authorization": f"Bearer {token}"} if token else {}

    async def get_user(self, user_id: str, token: str):
        url = f"{config.USER_MGMT_URL}/user/{user_id}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def create_user(self, user_data: dict, token: str):
        url = f"{config.USER_MGMT_URL}/user"
        response = await self.client.post(url, json=user_data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def authenticate_user(self, email: str, password: str, token: str):
        url = f"{config.USER_MGMT_URL}/user/authenticate"
        response = await self.client.post(url, data={"email": email, "password": password}, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def modify_user(self, user_id: str, user_data: dict, token: str):
        url = f"{config.USER_MGMT_URL}/user"
        user_data["UID"] = user_id
        response = await self.client.put(url, json=user_data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def delete_user(self, user_id: str, token: str):
        url = f"{config.USER_MGMT_URL}/user/{user_id}"
        response = await self.client.delete(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def get_event(self, event_id: str, token: str):
        url = f"{config.EVENT_MGMT_URL}/events/{event_id}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def get_all_events(self, limit: int = 1, offset: int = 10, token: str = ""):
        url = f"{config.EVENT_MGMT_URL}/events?limit={limit}&offset={offset}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def create_event(self, event_data: dict, token: str):
        url = f"{config.EVENT_MGMT_URL}/events"
        response = await self.client.post(url, json=event_data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def update_event(self, event_data: dict, token: str):
        url = f"{config.EVENT_MGMT_URL}/events"
        response = await self.client.put(url, json=event_data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def patch_event_guests(self, event_id: str, guests_remaining: int, token: str):
        url = f"{config.EVENT_MGMT_URL}/events/{event_id}/guests_remaining"
        data = {"guests_remaining": guests_remaining}
        response = await self.client.patch(url, json=data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def delete_event(self, event_id: str, token: str):
        url = f"{config.EVENT_MGMT_URL}/events/{event_id}"
        response = await self.client.delete(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def book_ticket(self, booking_data: dict, token: str):
        url = f"{config.TICKET_URL}/ticket"
        response = await self.client.post(url, json=booking_data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def cancel_ticket(self, booking_id: str, token: str):
        url = f"{config.TICKET_URL}/ticket/{booking_id}"
        response = await self.client.delete(url, headers=self._get_headers(token))
        response.raise_for_status()
        return {"message": "Event booking canceled successfully"}

    async def fetch_ticket(self, booking_id: str, token: str):
        url = f"{config.TICKET_URL}/ticket/{booking_id}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def get_tickets_by_user(self, user_id: str, token: str):
        url = f"{self.config.TICKET_URL}/ticket?uid={user_id}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()


    async def get_organizer(self, organizer_id: str, token: str):
        url = f"{self.config.USER_MGMT_URL}/organizer/{organizer_id}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def create_organizer(self, organizer_data: dict, token: str):
        url = f"{self.config.USER_MGMT_URL}/organizer"
        response = await self.client.post(url, json=organizer_data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def modify_organizer(self, organizer_id: str, organizer_data: dict, token: str):
        url = f"{self.config.USER_MGMT_URL}/organizer/{organizer_id}"
        response = await self.client.put(url, json=organizer_data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def delete_organizer(self, organizer_id: str, token: str):
        url = f"{self.config.USER_MGMT_URL}/organizer/{organizer_id}"
        response = await self.client.delete(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def get_user_by_email(self, email: str, token: str):
        url = f"{self.config.USER_MGMT_URL}/user"
        response = await self.client.get(url, params={"email": email}, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()
        
    async def get_tickets_and_events(self, user_id: str, limit: int = 10, offset: int = 0, token: str = ""):
        tickets_coroutine = self.get_tickets_by_user(user_id, token)
        events_coroutine = self.get_all_events(limit=limit, offset=offset, token=token)
        tickets_result, events_result = await asyncio.gather(tickets_coroutine, events_coroutine)
        events = events_result.get("events", [])

        has_next = len(events) > limit
        if has_next:
            events = events[:limit]

        has_prev = offset > 0

        events_pagination = {
            "limit": limit,
            "offset": offset,
            "has_next": has_next,
            "has_prev": has_prev
        }

        return {
            "tickets": tickets_result.get("tickets", []),
            "events": events,
            "events_pagination": events_pagination
        }
