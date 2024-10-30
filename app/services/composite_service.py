import httpx
from app.utils.config import Config
import asyncio

config = Config()

class CompositeService:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.config = Config()

    async def get_user(self, user_id: str):
        url = f"{config.USER_MGMT_URL}/user/{user_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def create_user(self, user_data: dict):
        url = f"{config.USER_MGMT_URL}/user"
        response = await self.client.post(url, json=user_data)
        response.raise_for_status()
        return response.json()

    async def authenticate_user(self, email: str, password: str):
        url = f"{config.USER_MGMT_URL}/user/authenticate"
        response = await self.client.post(url, data={"email": email, "password": password})
        response.raise_for_status()
        return response.json()

    async def modify_user(self, user_id: str, user_data: dict):
        url = f"{config.USER_MGMT_URL}/user"
        user_data["UID"] = user_id
        response = await self.client.put(url, json=user_data)
        response.raise_for_status()
        return response.json()

    async def delete_user(self, user_id: str):
        url = f"{config.USER_MGMT_URL}/user/{user_id}"
        response = await self.client.delete(url)
        response.raise_for_status()
        return response.json()

    async def get_event(self, event_id: str):
        url = f"{config.EVENT_MGMT_URL}/events/{event_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_all_events(self, limit: int = 1, offset: int = 10):
        url = f"{config.EVENT_MGMT_URL}/events?limit={limit}&offset={offset}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def create_event(self, event_data: dict):
        url = f"{config.EVENT_MGMT_URL}/events"
        response = await self.client.post(url, json=event_data)
        response.raise_for_status()
        return response.json()

    async def update_event(self, event_data: dict):
        url = f"{config.EVENT_MGMT_URL}/events"
        response = await self.client.put(url, json=event_data)
        response.raise_for_status()
        return response.json()

    async def delete_event(self, event_id: str):
        url = f"{config.EVENT_MGMT_URL}/events/{event_id}"
        response = await self.client.delete(url)
        response.raise_for_status()
        return response.json()

    async def book_ticket(self, booking_data: dict):
        url = f"{config.TICKET_URL}/ticket"
        response = await self.client.post(url, json=booking_data)
        response.raise_for_status()
        return response.json()

    async def cancel_ticket(self, booking_id: str):
        url = f"{config.TICKET_URL}/ticket/{booking_id}"
        response = await self.client.delete(url)
        response.raise_for_status()
        return {"message": "Event booking canceled successfully"}

    async def fetch_ticket(self, booking_id: str):
        url = f"{config.TICKET_URL}/ticket/{booking_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_tickets_by_user(self, user_id: str):
        url = f"{self.config.TICKET_URL}/ticket?uid={user_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_tickets_and_events(self, user_id: str):
        #Fetches all tickets for a specific user and all events asynchronously.
        try:
            tickets_coroutine = self.get_tickets_by_user(user_id)
            events_coroutine = self.get_all_events()
            tickets_result, events_result = await asyncio.gather(tickets_coroutine, events_coroutine)

            return {
                "tickets": tickets_result.get("tickets", []),
                "events": events_result.get("events", [])
            }

        except Exception as e:
            raise e

    async def close(self):
        await self.client.aclose()
