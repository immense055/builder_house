import requests
import socket


def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    data = response.json()

    return {
        "bitcoin": "BTC",
        "price_usd": data["bitcoin"]["usd"]
    }


def get_bitcoin_network():
    return {
        "network": "Bitcoin Mainnet",
        "type": "Proof of Work",
        "status": "active"
    }


def get_latest_block():
    url = "https://blockchain.info/latestblock"

    response = requests.get(
        url,
        timeout=10
    )

    data = response.json()

    return {
        "height": data["height"],
        "hash": data["hash"],
        "time": data["time"]
    }


def get_address_info(address):
    url = f"https://blockchain.info/rawaddr/{address}"

    response = requests.get(
        url,
        timeout=10
    )

    data = response.json()

    return {
        "address": address,
        "balance_btc": data["final_balance"] / 100000000,
        "total_received_btc": data["total_received"] / 100000000,
        "total_sent_btc": data["total_sent"] / 100000000,
        "transaction_count": data["n_tx"]
    }
def check_address(address):

    url = f"https://blockchain.info/rawaddr/{address}"

    response = requests.get(
        url,
        timeout=10
    )

    if response.status_code != 200:
        return {
            "address": address,
            "valid": False,
            "status": "Invalid or unavailable address"
        }

    data = response.json()

    balance = data["final_balance"] / 100000000
    tx_count = data["n_tx"]

    risk = "low"

    if tx_count > 1000:
        risk = "active_address"

    if balance > 100:
        risk = "high_value_wallet"

    return {
        "address": address,
        "valid": True,
        "balance_btc": balance,
        "transaction_count": tx_count,
        "risk_level": risk
    }
def get_transaction_info(txid):

    url = f"https://blockchain.info/rawtx/{txid}"

    response = requests.get(
        url,
        timeout=10
    )

    data = response.json()

    return {
        "txid": data["hash"],
        "size": data["size"],
        "block_height": data.get("block_height"),
        "fee_btc": data.get("fee", 0) / 100000000,
        "inputs": len(data["inputs"]),
        "outputs": len(data["out"])
    }

def get_block_info(block_hash):

    url = f"https://blockchain.info/rawblock/{block_hash}"

    response = requests.get(
        url,
        timeout=10
    )

    data = response.json()

    latest_height = get_latest_block()["height"]

    confirmations = 0

    if data.get("height"):
        confirmations = latest_height - data["height"] + 1

    return {
        "hash": data["hash"],
        "height": data["height"],
        "confirmations": confirmations,
        "time": data["time"],
        "tx_count": len(data.get("tx", []))
    }
def get_mempool_info():

    url = "https://blockchain.info/unconfirmed-transactions?format=json"

    response = requests.get(
        url,
        timeout=10
    )

    data = response.json()

    transactions = data.get("txs", [])

    return {
        "network": "Bitcoin Mainnet",
        "pending_transactions": len(transactions),
        "status": "active"
    }

def get_fee_estimate():

    url = "https://api.blockchain.info/mempool/fees"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    return {
        "source": "blockchain.info",
        "slow": data["limits"]["min"],
        "medium": data["regular"],
        "fast": data["limits"]["max"],
        "unit": "sat/vB"
    }

def broadcast_transaction(raw_tx):

    url = "https://blockstream.info/api/tx"

    headers = {
        "Content-Type": "text/plain"
    }

    response = requests.post(
        url,
        data=raw_tx,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    return {
        "status": "broadcasted",
        "txid": response.text
    }
