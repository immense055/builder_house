import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VIABTC_API_KEY")
API_SECRET = os.getenv("VIABTC_API_SECRET")

BASE_URL = "https://www.viabtc.com"


def sign(params):
    """
    ViaBTC signature
    """

    query = "&".join(
        f"{k}={params[k]}"
        for k in sorted(params)
    )

    return hmac.new(
        API_SECRET.encode("utf-8"),
        query.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def request_api(path, params=None):

    if params is None:
        params = {}

    params["access_id"] = API_KEY
    params["tonce"] = str(int(time.time() * 1000))

    params["signature"] = sign(params)

    url = BASE_URL + path

    r = requests.get(
        url,
        params=params,
        timeout=10
    )

    return r.json()



def get_hashrate():

    return request_api(
        "/res/openapi/v1/hashrate",
        {
            "coin": "BTC"
        }
    )



def get_workers():

    return request_api(
        "/res/openapi/v1/hashrate/worker",
        {
            "coin": "BTC"
        }
    )
def get_live_hashrate():

    url = BASE_URL + "/res/openapi/v1/hashrate"

    params = {
        "coin": "BTC"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    return response.json()
