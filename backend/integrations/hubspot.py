import json
import secrets
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import base64
import requests
from integrations.integration_item import IntegrationItem
from redis_client import add_key_value_redis, get_value_redis, delete_key_redis
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv('HUBSPOT_CLIENT_ID')
CLIENT_SECRET = os.getenv('HUBSPOT_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/integrations/hubspot/oauth2callback'
authorization_url = f'https://app-na2.hubspot.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=oauth%20crm.objects.contacts.read'

encoded_client_id_secret = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()

async def authorize_hubspot(user_id, org_id):
    state_data = {
        'state': secrets.token_urlsafe(32),
        'user_id': user_id,
        'org_id': org_id
    }
    encoded_state = json.dumps(state_data)
    await add_key_value_redis(f'hubspot_state:{org_id}:{user_id}', encoded_state, expire=600)

    return f'{authorization_url}&state={encoded_state}'

async def oauth2callback_hubspot(request: Request):
    if request.query_params.get('error'):
        raise HTTPException(status_code=400, detail=request.query_params.get('error'))
    code = request.query_params.get('code')
    encoded_state = request.query_params.get('state')
    state_data = json.loads(encoded_state)

    original_state = state_data.get('state')
    user_id = state_data.get('user_id')
    org_id = state_data.get('org_id')

    saved_state = await get_value_redis(f'hubspot_state:{org_id}:{user_id}')

    if not saved_state or original_state != json.loads(saved_state).get('state'):
        raise HTTPException(status_code=400, detail='State does not match.')

    async with httpx.AsyncClient() as client:
        response, _ = await asyncio.gather(
            client.post(
                'https://api.hubapi.com/oauth/v1/token',
                data={
                    'grant_type': 'authorization_code',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'redirect_uri': REDIRECT_URI,
                    'code': code,
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            ),
            delete_key_redis(f'hubspot_state:{org_id}:{user_id}'),
        )

    await add_key_value_redis(f'hubspot_credentials:{org_id}:{user_id}', json.dumps(response.json()), expire=600)
    
    close_window_script = """
    <html>
        <script>
            window.close();
        </script>
    </html>
    """
    return HTMLResponse(content=close_window_script)

async def get_hubspot_credentials(user_id, org_id):
    credentials = await get_value_redis(f'hubspot_credentials:{org_id}:{user_id}')
    if not credentials:
        raise HTTPException(status_code=400, detail='No credentials found.')
    credentials = json.loads(credentials)
    await delete_key_redis(f'hubspot_credentials:{org_id}:{user_id}')

    return credentials

def create_integration_item_metadata_object(response_json):
    """Creates an integration metadata object from a HubSpot contact"""
    integration_item_metadata = IntegrationItem(
        id=response_json.get('id', None),
        name=response_json.get('properties', {}).get('firstname', '') + ' ' + response_json.get('properties', {}).get('lastname', ''),
        type='Contact',
        parent_id=None,
        parent_path_or_name=None,
        creation_time=response_json.get('createdAt', None),
        last_modified_time=response_json.get('updatedAt', None),
    )
    return integration_item_metadata

async def get_items_hubspot(credentials) -> list[dict]:
    """Aggregates all metadata relevant for a HubSpot integration (contacts) and returns as list of dicts."""
    credentials = json.loads(credentials) if isinstance(credentials, str) else credentials
    if not credentials or 'access_token' not in credentials:
        raise HTTPException(status_code=400, detail='Invalid credentials.')
    access_token = credentials.get('access_token')
    url = 'https://api.hubapi.com/crm/v3/objects/contacts'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    items = []
    if response.status_code == 200:
        results = response.json().get('results', [])
        for result in results:
            item = create_integration_item_metadata_object(result)
            items.append(item.__dict__)
        print(items)  # Optional: for debugging
    else:
        print(f'Error fetching HubSpot items: {response.text}')
    return items