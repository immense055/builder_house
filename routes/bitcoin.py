from flask import Blueprint, jsonify, request

from services.bitcoin_service import (
    get_bitcoin_price,
    get_bitcoin_network,
    get_latest_block,
    get_address_info,
    get_transaction_info,
    get_block_info,
    get_mempool_info,
    get_fee_estimate,
    broadcast_transaction
)

from middleware.api_key import require_api_key

bitcoin = Blueprint("bitcoin", __name__)


@bitcoin.route("/bitcoin/price", methods=["GET"])
def price():
    check = require_api_key()
    if check:
        return check

    return jsonify(get_bitcoin_price())


@bitcoin.route("/bitcoin/network", methods=["GET"])
def network():
    return jsonify(get_bitcoin_network())


@bitcoin.route("/bitcoin/latest-block", methods=["GET"])
def latest_block():
    return jsonify(get_latest_block())

@bitcoin.route("/bitcoin/tx/<txid>", methods=["GET"])
def transaction(txid):
    try:
        data = get_transaction_info(txid)
        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@bitcoin.route("/bitcoin/block/<block_hash>", methods=["GET"])
def block_info(block_hash):

    try:
        data = get_block_info(block_hash)
        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@bitcoin.route("/bitcoin/mempool", methods=["GET"])
def mempool():

    return jsonify(get_mempool_info())

@bitcoin.route("/bitcoin/fees", methods=["GET"])
def fees():

    return jsonify(get_fee_estimate())

@bitcoin.route("/bitcoin/broadcast", methods=["POST"])
def broadcast():

    body = request.get_json()

    raw_tx = body.get("raw_tx")

    if not raw_tx:
        return jsonify({
            "error": "raw_tx is required"
        }), 400

    try:
        return jsonify(
            broadcast_transaction(raw_tx)
        )

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
