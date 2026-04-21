def validate_symbol(symbol: str) -> str:
    """
    Ensures symbol strictly follows the USDT testnet pair convention.
    """
    upper_symbol = symbol.upper().strip()
    if not upper_symbol.endswith("USDT"):
        raise ValueError("Only USDT-M futures pairs are fully supported by this example (e.g., BTCUSDT).")
    return upper_symbol

def validate_side(side: str) -> str:
    """
    Restricts action vectors.
    """
    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Order side must be BUY or SELL.")
    return side

def validate_order_type(order_type: str, price: float) -> str:
    """
    Checks that core mechanics match the order context.
    """
    order_type = order_type.upper().strip()
    
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("This version only supports MARKET and LIMIT order types.")
    
    if order_type == "LIMIT" and (price is None or price <= 0):
        # We will catch this in CLI prompt logic too, but it resides here as strict business logic defense
        raise ValueError("LIMIT orders strictly require a target price greater than 0.")
        
    return order_type
