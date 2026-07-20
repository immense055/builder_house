import requests

TRON_API = "https://api.trongrid.io"

def get_wallet_balance(address):
    url = f"{TRON_API}/v1/accounts/{address}"
    response = requests.get(url, timeout=10)
    return response.json()
