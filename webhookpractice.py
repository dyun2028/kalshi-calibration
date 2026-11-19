import requests
import websockets
import asyncio
import json
import time
import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
with open("kalshi_private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(), password=None
    )

def get_headers(API_KEY: str, path: str, method="GET"):
    path = path.split("?")[0]
    timestamp = str(int(time.time() * 1000))
    message = (timestamp + method + path).encode("utf-8")

    if isinstance(private_key, ed25519.Ed25519PrivateKey):
        signature = private_key.sign(message)
    else:
        raise ValueError("Not ED25519")

    signature = base64.b64encode(signature).decode("utf-8")

    return {
        "KALSHI-ACCESS-KEY": API_KEY,
        "KALSHI-ACCESS-SIGNATURE": signature,
        "KALSHI-ACCESS-TIMESTAMP": timestamp
    }
auth_headers = get_headers("db709c9d-c776-4e87-8638-ee53c0ce1c75", "/trade-api/ws/v2", "GET")
#print(auth_headers)
url = f"wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2"
async def connect():
    async with websockets.connect(url, additional_headers=auth_headers) as ws:
        print("connected to demo site")
        async for message in ws:
            print(f"Received {message}")

asyncio.run(connect())