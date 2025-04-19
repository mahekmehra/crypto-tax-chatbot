import requests
from datetime import datetime

def get_crypto_price(coin_id, date=None, currency="usd"):
    base_url = "https://api.coingecko.com/api/v3"
    if date:
        try:
            # Historical price
            date_obj = datetime.strptime(date, "%d-%m-%Y")
            endpoint = f"{base_url}/coins/{coin_id}/history"
            params = {"date": date_obj.strftime("%d-%m-%Y"), "localization": "false"}
        except ValueError:
            return "Invalid date format. Use DD-MM-YYYY."
    else:
        # Current price
        endpoint = f"{base_url}/simple/price"
        params = {"ids": coin_id, "vs_currencies": currency}

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        if date:
            price = data["market_data"]["current_price"][currency.lower()]
        else:
            price = data[coin_id][currency.lower()]
        return price
    except requests.RequestException as e:
        return f"Failed to fetch price from CoinGecko: {str(e)}"
    except KeyError:
        return f"Price unavailable for {coin_id} in {currency}."