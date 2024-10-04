import os

import httpx
from fastapi import APIRouter, HTTPException

KEY = os.getenv("REG_KEY")
URL = os.getenv("URL")

router = APIRouter()


# Function to call the BLS API
async def fetch_bls_series_data(series_id: str = "SUUR0000SA0", start_year: int = 2018, end_year: int = 2022):
    params = {
        "seriesid": [series_id],
        "startyear": start_year,
        "endyear": end_year,
        "catalog": True,
        "calculations": True,
        "registrationkey": KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(URL, json=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error fetching data from BLS API",
            )
