import re
from crypto_api import get_crypto_price
from tax_calculator import calculate_tax

# Supported cryptocurrencies
CRYPTO_MAP = {
    "btc": "bitcoin",
    "eth": "ethereum",
    # Add more as needed
}

def chatbot_response(user_input):
    """Generate a response based on user input."""
    user_input = user_input.lower().strip()
    
    # Keywords for tax or price queries
    tax_keywords = ["tax", "gain", "loss", "calculate", "sold", "bought"]
    price_keywords = ["price", "value", "worth"]
    
    # Check if it's a crypto-related question
    if any(keyword in user_input for keyword in tax_keywords + price_keywords):
        # Identify the cryptocurrency
        crypto = None
        for symbol, name in CRYPTO_MAP.items():
            if symbol in user_input or name in user_input:
                crypto = name
                break
        
        if not crypto:
            return "Please specify a cryptocurrency (e.g., BTC, ETH)."
        
        # Handle price queries
        if any(keyword in user_input for keyword in price_keywords):
            date_match = re.search(r'on (\d{1,2}-\d{1,2}-\d{4})', user_input)
            date = date_match.group(1) if date_match else None
            price = get_crypto_price(crypto, date)
            return f"The price of {crypto.capitalize()} was ${price:.2f} on {date or 'today'}."
        
        # Handle tax calculations
        if any(keyword in user_input for keyword in tax_keywords):
            numbers = re.findall(r'\d+\.?\d*', user_input)
            dates = re.findall(r'\d{1,2}-\d{1,2}-\d{4}', user_input)
            
            if len(numbers) >= 3:
                quantity, buy_price, sell_price = map(float, numbers[:3])
                buy_date, sell_date = (dates + [None, None])[:2]  # Use dates if provided
                gain, tax = calculate_tax(buy_price, sell_price, quantity, buy_date, sell_date)
                return f"Your gain/loss: ${gain:.2f}. Estimated tax: ${tax:.2f}."
            return "Please provide quantity, buy price, and sell price (e.g., 'I sold 1 BTC at 60000 after buying at 50000')."
    
    # Out of scope response
    return "This is out of my scope."

# Main loop
if __name__ == "__main__":
    print("Welcome to the Crypto Tax Calculator Chatbot!")
    print("Ask me about crypto prices or taxes (e.g., 'What’s my tax if I sold 1 BTC at 60000 after buying at 50000?')")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chatbot_response(user_input)
        print(f"Bot: {response}")