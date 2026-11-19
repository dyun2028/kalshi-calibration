import requests
import json

url = "https://external-api.kalshi.com/trade-api/v2/series/KXHIGHNY"
response = requests.get(url)
series_data = response.json()
print(series_data)

with open("output.json", "w") as f:
    json.dump(series_data, f, indent=4)

markets_url = f"https://external-api.kalshi.com/trade-api/v2/markets?series_ticker=KXHIGHNY&status=open"
markets_response = requests.get(markets_url)
markets_data = markets_response.json()

with open ("markets.json", "w") as f:
    json.dump(markets_data, f, indent=4)
print(f'\nActive Markets in KXHIGHNY')
for market in markets_data["markets"]:
    print(f'Ticker {market["title"]}')
    print(f'Ticker {market["ticker"]}')
    print(f'Ticker {market["status"]}')
print()
print()

if not markets_data["markets"]:
    raise ValueError("no markets")
event_ticker = markets_data["markets"][0]["event_ticker"]
print(f'Markets thing {markets_data["markets"][1]["status"]}')

event_url = f"https://external-api.kalshi.com/trade-api/v2/events/{event_ticker}"
event_response = requests.get(event_url)
event_data = event_response.json()
print(f"Event Details:")
print(f'Title: {event_data['event']['title']}')
print(f'Category: {event_data['event']['category']}')

ticker = markets_data["markets"][0]["ticker"]
orderbook_url = f"https://external-api.kalshi.com/trade-api/v2/markets/{ticker}/orderbook"
print(orderbook_url)
orderbook_response = requests.get(orderbook_url)
try:
    orderbook_data = orderbook_response.json()
except:
    raise ValueError("no response orderbook")

with open("orderbook.json", "w") as f:
    json.dump(orderbook_data, f, indent=4)
print(f"YES\n")