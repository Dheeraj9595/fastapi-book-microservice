import os
import httpx
from .models import Author
from fastapi import HTTPException


AUTHOR_SERVICE_HOST_URL = os.environ.get("AUTHOR_SERVICE_HOST_URL")

url = AUTHOR_SERVICE_HOST_URL

def is_author_present(author_id: int):
    r = httpx.get(f"{url}{author_id}/")
    return True if r.status_code == 200 else False

async def fetch_author(author_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTHOR_SERVICE_HOST_URL}{author_id}/")
        if response.status_code == 200:
            return Author(**response.json())
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")