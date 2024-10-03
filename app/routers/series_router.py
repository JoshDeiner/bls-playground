from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.series import SeriesRequest
from app.services.bls_service import fetch_bls_series_data
from app.services.series_service import upsert_series

router = APIRouter()

# API to handle series data updates


# this is probably not right. on the post we hit the 3rd party
# probably at least need to pass in an ID
@router.post("/series")
def update_series(series_request: SeriesRequest, db: Session = Depends(get_db)):
    try:
        upsert_series(db, series_request)
        return {"status": "success", "message": "Series data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# probably doesnt work above. need the request object somewhere. need to figure out.
# but overall probably done for now. map out what your plan for tomorrow is. and then end of the day maybe you can do
# 1 more hour okay

# i think you're pretty close to getting the dummy data inserted which is great

# async def bls_response():
#     url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
#     payload = {
#         #    inputs are start year, endyear
#         # maybe you stream it
#         "seriesid": ["SUUR0000SA0"],
#         "startyear": "2018",
#         "endyear":"2022",
#         "catalog": True,
#         "calculations": True,
#         "registrationkey": KEY
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, json=payload)

#     # Return the response from the third-party API or your own message
#     return {"status": response.status_code, "data": response.json()}
