import os
import httpx

from fastapi import HTTPException

KEY = os.getenv("REG_KEY")

router = APIRouter()


# Function to call the BLS API
def fetch_bls_series_data(series_id: str = "SUUR0000SA0"):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    params = {
        "seriesid": [series_id],
        # "seriesid": ["SUUR0000SA0"],
        "startyear": "2018",
        "endyear": "2022",
        "catalog": True,
        "calculations": True,
        "registrationkey": KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error fetching data from BLS API",
            )
