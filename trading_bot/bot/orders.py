from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.client import BinanceFuturesClient
from bot.logging_config import logger

class OrderManager:
    """
    Encapsulates trading logic specific to futures execution.
    """
    def __init__(self, client_wrapper: BinanceFuturesClient):
        self.client = client_wrapper.api

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        """
        Places a raw order request via the Binance client.
        Catches API exceptions gracefully and logs outcomes.
        """
        try:
            logger.info(f"Attempting {order_type} {side} order for {quantity} {symbol} at price {'MARKET' if price is None else price}")

            # Base parameters required for all order types
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }

            # Inject parameters specific to LIMIT type
            if order_type == "LIMIT":
                params["timeInForce"] = "GTC"  # Need specifying for LIMIT orders (Good Till Cancel)
                params["price"] = price

            # We use futures_create_order specifically for USDT-M Futures interactions
            response = self.client.futures_create_order(**params)

            logger.info(f"Order Success! ID: {response.get('orderId')}, Status: {response.get('status')}")
            logger.debug(f"Full response: {response}")

            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API Refusal: {e.status_code} - {e.message}")
        except BinanceRequestException as e:
            logger.error(f"Network error while communicating with Binance: {e}")
        except Exception as e:
            logger.error(f"Unexpected system error during order execution: {e}")

        return None
