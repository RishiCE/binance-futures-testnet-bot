import os
from binance.client import Client
from bot.logging_config import logger

class BinanceFuturesClient:
    """
    A wrapper around the python-binance client, securely initializing API 
    keys from the environment. Supports both standard HMAC and Ed25519/RSA keys.
    """
    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        private_key_path = os.getenv("BINANCE_PRIVATE_KEY_PATH")

        if not api_key:
            logger.error("BINANCE_API_KEY not found in environment variables.")
            raise EnvironmentError("Please set your BINANCE_API_KEY.")

        if not api_secret and not private_key_path:
            logger.error("No secret provided. Use BINANCE_API_SECRET or BINANCE_PRIVATE_KEY_PATH.")
            raise EnvironmentError("Please set either BINANCE_API_SECRET (HMAC) or BINANCE_PRIVATE_KEY_PATH (Ed25519/RSA).")

        try:
            kwargs = {"api_key": api_key, "testnet": True}
            
            # Ed25519 / RSA flow
            if private_key_path:
                if not os.path.exists(private_key_path):
                    raise FileNotFoundError(f"Private key file not found at: {private_key_path}")
                with open(private_key_path, 'r') as f:
                    private_key_str = f.read()
                
                kwargs["private_key"] = private_key_str
                logger.info("Using Ed25519/RSA Private Key for authentication.")
            
            # Standard HMAC flow
            else:
                kwargs["api_secret"] = api_secret
                logger.info("Using standard HMAC Secret Key for authentication.")

            # Initialize
            self._client = Client(**kwargs)
            logger.info("Binance client initialized for testnet.")
            
        except Exception as e:
            logger.error(f"Failed to initialize Binance Client: {e}")
            raise

    @property
    def api(self) -> Client:
        return self._client
