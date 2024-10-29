import httpx
from app.utils.config import Config

config = Config()

class CompositeService:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get_user(self, user_id: str):
        url = f"{config.USER_MGMT_URL}/users/{user_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def create_user(self, user_data: dict):
        url = f"{config.USER_MGMT_URL}/users/createUser"
        response = await self.client.post(url, json=user_data)
        response.raise_for_status()
        return response.json()

    async def authenticate_user(self, email: str, password: str):
        url = f"{config.USER_MGMT_URL}/users/authenticate"
        response = await self.client.post(url, data={"email": email, "password": password})
        response.raise_for_status()
        return response.json()

    async def modify_user(self, user_id: str, user_data: dict):
        url = f"{config.USER_MGMT_URL}/users/modifyUser"
        user_data["UID"] = user_id
        response = await self.client.put(url, json=user_data)
        response.raise_for_status()
        return response.json()

    async def get_event(self, event_id: str):
        url = f"{config.EVENT_MGMT_URL}/events/{event_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_all_events(self, page: int = 1, size: int = 10):
        url = f"{config.EVENT_MGMT_URL}/events?page={page}&size={size}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def create_event(self, event_data: dict):
        url = f"{config.EVENT_MGMT_URL}/events"
        response = await self.client.post(url, json=event_data)
        response.raise_for_status()
        return response.json()

    async def update_event(self, event_id: str, event_data: dict):
        url = f"{config.EVENT_MGMT_URL}/events/{event_id}"
        response = await self.client.put(url, json=event_data)
        response.raise_for_status()
        return response.json()

    async def delete_event(self, event_id: str):
        url = f"{config.EVENT_MGMT_URL}/events/{event_id}"
        response = await self.client.delete(url)
        response.raise_for_status()
        return response.json()

    async def book_event_booking(self, booking_data: dict):
        url = f"{config.EVENT_BOOKING_URL}/tickets/"  # Assuming the endpoint remains /tickets/
        response = await self.client.post(url, json=booking_data)
        response.raise_for_status()
        return response.json()

    async def cancel_event_booking(self, booking_id: str):
        url = f"{config.EVENT_BOOKING_URL}/tickets/{booking_id}"
        response = await self.client.delete(url)
        response.raise_for_status()
        return {"message": "Event booking canceled successfully"}

    async def fetch_event_booking(self, booking_id: str):
        url = f"{config.EVENT_BOOKING_URL}/tickets/{booking_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()
