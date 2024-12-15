import json
import os
from typing import List

import httpx
from app.utils.config import Config
import asyncio
import boto3

config = Config()

class CompositeService:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.config = Config()

        self.lambda_client = boto3.client('lambda', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        self.lambda_function_name = os.getenv('SEND_EMAIL_LAMBDA_FUNCTION_NAME')
        self.sns_client = boto3.client('sns', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        self.sns_topic_arn = os.getenv('EVENT_UPDATED_SNS_TOPIC_ARN')

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

    async def get_all_events(self, limit: int = 10, offset: int = 0, token: str = ""):
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


    async def get_organiser(self, organiser_id: str, token: str):
        url = f"{self.config.USER_MGMT_URL}/organiser/{organiser_id}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def create_organiser(self, organiser_data: dict, token: str):
        url = f"{self.config.USER_MGMT_URL}/organiser"
        response = await self.client.post(url, json=organiser_data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def modify_organiser(self, organiser_id: str, organiser_data: dict, token: str):
        url = f"{self.config.USER_MGMT_URL}/organiser/{organiser_id}"
        response = await self.client.put(url, json=organiser_data, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def delete_organiser(self, organiser_id: str, token: str):
        url = f"{self.config.USER_MGMT_URL}/organiser/{organiser_id}"
        response = await self.client.delete(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def get_user_by_email(self, email: str, token: str):
        url = f"{self.config.USER_MGMT_URL}/user"
        response = await self.client.get(url, params={"email": email}, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()
    
    async def get_organiser_by_email(self, email: str, token: str):
        url = f"{self.config.USER_MGMT_URL}/organiser"
        response = await self.client.get(url, params={"email": email}, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()
        
    async def get_tickets_and_events(self, user_id: str, limit: int = 10, offset: int = 0, token: str = ""):
        tickets_coroutine = self.get_tickets_by_user(user_id, token)
        events_coroutine = self.get_all_events(limit=limit, offset=offset, token=token)
        tickets_result, events_result = await asyncio.gather(tickets_coroutine, events_coroutine)
        events = events_result['result']['data']

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

    async def get_events_by_organizer(self, oid: str, limit: int, offset: int, token: str) -> List[dict]:
        url = f"{config.EVENT_MGMT_URL}/events/organizer/{oid}?limit={limit}&offset={offset}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def update_guests_remaining(self, eid: str, guests_remaining: int, token: str) -> dict:
        url = f"{config.EVENT_MGMT_URL}/events/{eid}/{guests_remaining}"
        response = await self.client.patch(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def get_users_by_event(self, eid: str, limit: int, offset: int, token: str) -> List[dict]:
        url = f"{config.TICKET_URL}/ticket/event/{eid}/users?limit={limit}&offset={offset}"
        response = await self.client.get(url, headers=self._get_headers(token))
        response.raise_for_status()
        return response.json()

    async def invoke_send_email_lambda(self, booking_details: dict):
        if not self.lambda_function_name:
            print("Lambda function name not configured.")
            return None
        try:
            payload = json.dumps({'body': booking_details })
            response = self.lambda_client.invoke(
                FunctionName=self.lambda_function_name,
                InvocationType='Event',
                Payload=payload.encode('utf-8')
            )
            return response
        except Exception as e:
            print(f"Failed to invoke Lambda function: {e}")
            return None

    async def publish_event_update_notification(self, message):
        if not self.sns_topic_arn:
            return None
        try:
            response = self.sns_client.publish(
                TopicArn=self.sns_topic_arn,
                Message=json.dumps(message),
                Subject='Event Updated Notification'
            )
            print(f"Published event update notification to SNS. Message ID: {response['MessageId']}")
            return response
        except Exception as e:
            print(f"Failed to publish event update notification: {e}")
            return None

