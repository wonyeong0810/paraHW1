from fastapi import APIRouter, HTTPException

import requests

coin = APIRouter(prefix="/coin")

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

@coin.get("/{coin_id}")
def get_crypto_price(coin_id: str):
    try:
        response = requests.get(COINGECKO_API_URL, params={"ids": coin_id, "vs_currencies": "usd"})
        response.raise_for_status()
        data = response.json()
        if coin_id in data:
            return {
                "coin_id": coin_id,
                "price_usd": data[coin_id]["usd"]
            }
        else:
            raise HTTPException(status_code=404, detail="Coin not found")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
