from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import httpx
import os
import aioredis

from contextlib import asynccontextmanager
from typing import AsyncIterator, Any
import orjson

import logging
from starlette.requests import Request
from starlette.responses import Response
import time

from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.coder import PickleCoder
from fastapi_cache.decorator import cache
from fastapi.encoders import jsonable_encoder
from fastapi_cache import Coder

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

from app.routers.series_router import router as series_router

load_dotenv()

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def request_key_builder(
    func,
    namespace: str = "",
    *,
    request: Request = None,
    response: Response = None,
    **kwargs,
):
    return ":".join(
        [
            namespace,
            request.method.lower(),
            request.url.path,
            repr(sorted(request.query_params.items())),
        ]
    )


async def get_bls_data(api_endpoint: str):
    logger.info(f"Fetching data from cache or API: {api_endpoint}")
    # Call to your BLS API goes here
    data = await bls_response()
    return data


class ORJsonCoder(Coder):
    @classmethod
    def encode(cls, value: Any) -> bytes:
        return orjson.dumps(
            value,
            default=jsonable_encoder,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )

    @classmethod
    def decode(cls, value: bytes) -> Any:
        return orjson.loads(value)


app = FastAPI()

app.include_router(series_router)

KEY = os.getenv("REG_KEY")


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.post("/inflation_all/")
async def bls_response():
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        #    inputs are start year, endyear
        # maybe you stream it
        "seriesid": ["SUUR0000SA0"],
        "startyear": "2018",
        "endyear": "2022",
        "catalog": True,
        "calculations": True,
        "registrationkey": KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    # Return the response from the third-party API or your own message
    return {"status": response.status_code, "data": response.json()}


# this is okay and mildly interesting

# you can send this to a frontend and have it plot out the data right
# it's not perfect right it's missing lot's like what to do with the data and what to show and groupings of the data
# a lot of that can be done on the client

# also if i want to expose an ai chatbot all i need to give it is an API

######## !!!!!!! so now what i would like to see if maybe can you cache this data and create some kind of strategy !!!!! ###

#### then present the API to be consumed by a llm model ####


#### TODO NEXT ADD logging. Why?

#### i want to see if you are actually caching or not

#### i want to eventually test the APIs and add automation and stop gaps for when you come close to failing the limit

#### what is a good philosophy for logging
