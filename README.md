# Integrations Technical Assessment

## Overview

This project is a multi-integration platform that allows users to connect their accounts from **Notion**, **Airtable**, and **HubSpot** using OAuth 2.0. After connecting, users can load and view items (contacts, tables, pages, etc.) from these services in a unified frontend.

## Tech Stack

- **Frontend:** React, Material UI, Axios
- **Backend:** FastAPI (Python), Requests, httpx, python-dotenv
- **State Management:** Redis (for OAuth state and credentials)
- **Authentication:** OAuth 2.0

## Features

- Connect to Notion, Airtable, or HubSpot via OAuth
- Securely store and retrieve credentials using Redis
- Load and display integration items in a formatted, resizable text field
- Switch between integrations and disconnect previous connections

## How It Works

1. **OAuth Flow:**  
   - User selects an integration and clicks "Connect".
   - OAuth flow is initiated; credentials are stored in Redis.
2. **Loading Items:**  
   - After connecting, user can load items from the selected integration.
   - Items are fetched from the third-party API and displayed in the frontend.
3. **Switching Integrations:**  
   - Selecting a new integration disconnects the previous one and prompts for a new connection.

## Setup

### Backend

1. Install dependencies:
    ```
    pip install fastapi uvicorn python-dotenv redis httpx requests
    ```
2. Create a `.env` file in `/backend` with your client IDs and secrets:
    ```
    HUBSPOT_CLIENT_ID=your_hubspot_client_id
    HUBSPOT_CLIENT_SECRET=your_hubspot_client_secret
    AIRTABLE_CLIENT_ID=your_airtable_client_id
    AIRTABLE_CLIENT_SECRET=your_airtable_client_secret
    NOTION_CLIENT_ID=your_notion_client_id
    NOTION_CLIENT_SECRET=your_notion_client_secret
    ```
3. Start Redis server:
    ```
    redis-server
    ```
4. Run backend:
    ```
    uvicorn main:app --reload
    ```

### Frontend

1. Install dependencies:
    ```
    npm install
    ```
2. Start frontend:
    ```
    npm run start
    ```

## Integrations

- **Notion:** Workspace for notes and databases. API used for searching and reading pages/databases.
- **Airtable:** Spreadsheet-database hybrid. API used for reading bases and tables.
- **HubSpot:** CRM platform. API used for reading contacts.

## Folder Structure

- `/backend/integrations/`  
  Contains integration logic for Notion, Airtable, and HubSpot.
- `/frontend/src/integrations/`  
  Contains React components for each integration.

## Why This Stack?

- **React & Material UI:** Fast, modern UI.
- **FastAPI:** Async, easy API development.
- **Redis:** Secure, fast temporary storage for sensitive OAuth data.
- **OAuth 2.0:** Secure authentication standard.

## Notes

- You must register your own OAuth apps with Notion, Airtable, and HubSpot to get client IDs and secrets.
- For local development, use `http://localhost:8000/integrations/<integration>/oauth2callback` as your redirect URI.

## License

MIT
