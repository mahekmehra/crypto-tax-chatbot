def calculate_tax(buy_price, sell_price, quantity, buy_date=None, sell_date=None):
    gain = (sell_price - buy_price) * quantity
    tax_rate = 0.20  # 20% tax rate
    tax = gain * tax_rate if gain > 0 else 0
    return gain, tax