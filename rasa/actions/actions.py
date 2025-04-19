import sys
sys.path.append("C:\\Users\\MAHEK MEHRA\\crypto-tax-chatbot")
from crypto_api import get_crypto_price
from tax_calculator import calculate_tax

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging

logging.basicConfig(level=logging.DEBUG)

class ActionGetPrice(Action):
    def name(self):
        return "action_get_price"

    def run(self, dispatcher, tracker, domain):
        crypto = tracker.get_slot("crypto")
        date = tracker.get_slot("date")
        currency = tracker.get_slot("currency")
        
        logging.debug(f"Slots - crypto: {crypto}, date: {date}, currency: {currency}")
        
        if not crypto:
            dispatcher.utter_message(text="Please specify a cryptocurrency (e.g., BTC, ETH).")
            return [SlotSet("crypto", None), SlotSet("date", None), SlotSet("currency", "USD")]

        crypto = crypto.lower()
        valid_currencies = ["usd", "inr"]
        # Handle "rupees" as INR
        user_message = tracker.latest_message.get("text", "").lower()
        if "rupees" in user_message or (currency and currency.lower() == "inr"):
            currency = "inr"
        elif not currency or currency.lower() not in valid_currencies:
            currency = "usd"
        else:
            currency = currency.lower()
        
        crypto_map = {"btc": "bitcoin", "eth": "ethereum"}
        coin_id = crypto_map.get(crypto, crypto)
        
        logging.debug(f"Calling get_crypto_price with coin_id: {coin_id}, date: {date}, currency: {currency}")
        try:
            price = get_crypto_price(coin_id, date, currency)
            logging.debug(f"Price returned: {price}")
            if isinstance(price, str):
                dispatcher.utter_message(text=price)
            else:
                currency_symbol = "₹" if currency == "inr" else "$"
                dispatcher.utter_message(text=f"The price of {coin_id.capitalize()} was {currency_symbol}{price:.2f} on {date or 'today'}.")
        except Exception as e:
            logging.error(f"Unexpected error in get_crypto_price: {str(e)}")
            dispatcher.utter_message(text=f"Error fetching price: {str(e)}")
        return [SlotSet("crypto", None), SlotSet("date", None), SlotSet("currency", "USD")]

class ActionCalculateTax(Action):
    def name(self):
        return "action_calculate_tax"

    def run(self, dispatcher, tracker, domain):
        crypto = tracker.get_slot("crypto")
        quantity = tracker.get_slot("quantity")
        buy_price = tracker.get_slot("buy_price")
        sell_price = tracker.get_slot("sell_price")
        date = tracker.get_slot("date")
        currency = tracker.get_slot("currency")
        
        user_message = tracker.latest_message.get("text", "").lower()
        if "inr" in user_message or "rupees" in user_message:
            currency = "inr"
        else:
            currency = currency or "USD"
        
        logging.debug(f"Slots - crypto: {crypto}, quantity: {quantity}, buy_price: {buy_price}, sell_price: {sell_price}, date: {date}, currency: {currency}")
        
        if not all([crypto, quantity, buy_price, sell_price]):
            dispatcher.utter_message(text="Please provide quantity, buy price, and sell price.")
            return [SlotSet("crypto", None), SlotSet("quantity", None), SlotSet("buy_price", None), SlotSet("sell_price", None), SlotSet("date", None), SlotSet("currency", "USD")]
        
        try:
            buy_price = float(buy_price)
            sell_price = float(sell_price)
            quantity = float(quantity)
        except ValueError as e:
            logging.error(f"Invalid number format: {str(e)}")
            dispatcher.utter_message(text=f"Invalid number format: {str(e)}")
            return [SlotSet("crypto", None), SlotSet("quantity", None), SlotSet("buy_price", None), SlotSet("sell_price", None), SlotSet("date", None), SlotSet("currency", "USD")]
        
        currency = currency.lower()
        if sell_price < buy_price:
            buy_price, sell_price = sell_price, buy_price
        
        gain, tax = calculate_tax(buy_price, sell_price, quantity, None, date)
        currency_symbol = "₹" if currency == "inr" else "$"
        dispatcher.utter_message(text=f"Your gain/loss: {currency_symbol}{gain:.2f}. Estimated tax: {currency_symbol}{tax:.2f}.")
        return [SlotSet("crypto", None), SlotSet("quantity", None), SlotSet("buy_price", None), SlotSet("sell_price", None), SlotSet("date", None), SlotSet("currency", "USD")]