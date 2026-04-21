# Binance Futures Testnet Bot

This is a simplified trading bot for placing MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M). It includes both a clean CLI interface and a lightweight UI (`gui.py`) built with Tkinter.

## 1. Testnet vs. Mainnet API

This bot is configured out-of-the-box for **Testnet** (paper trading with simulated funds).

*   **Testnet API (Safe & Simulated):**
    *   **Purpose:** Development, learning, and testing algorithms without financial risk.
    *   **Portal:** `https://testnet.binancefuture.com`
    *   **Funding:** You receive virtual USDT upon creating the Testnet account.
    *   **API Keys:** Your keys must be generated specifically directly inside the Testnet dashboard. Real Binance keys will not work here.
*   **Mainnet API (Real Live Trading):**
    *   **Purpose:** Trading with actual cryptocurrency and real financial risk.
    *   **Portal:** `https://www.binance.com` -> Profile -> API Management
    *   **How to Switch:** If you decide to transition this bot to use real money, you will need to open `trading_bot/bot/client.py`, change `testnet=True` to `testnet=False`, and use your real Mainnet API keys. **Proceed with extreme caution!**

## 2. Prerequisites
- **Python:** Python 3.8 to 3.12 is highly recommended. (Python 3.14 alpha has known compatibility issues with networking libraries).
- **Testnet Account:** A Binance Futures Testnet account.

## 3. API Key Generation
You can use either a standard **HMAC** key or a more secure **Ed25519 / RSA** key.
1. Go to the [Binance Futures Testnet](https://testnet.binancefuture.com/) site.
2. Click "Create API Key".
   * **For HMAC:** Choose "System Generated". Binance provides both the API Key and Secret Key. Copy them immediately before closing the window.
   * **For Ed25519 / RSA (Recommended):** Choose "Self-generated". **Note: Binance does NOT generate these for you.** You must use a local tool (like the official Binance Desktop Key Generator, OpenSSL, or ssh-keygen) to create a key pair. You then copy the **Public Key** and paste it into the Binance website. Store your **Private Key** text locally by saving it into a file named `private_key.pem` inside this project folder.

## 4. Local Setup & Environment
1. Extract the downloaded ZIP file and open the root folder.
2. Open your Terminal (or Command Prompt / PowerShell) and navigate into the folder.
3. **Create and activate a virtual environment:**
   * **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **Mac / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
4. **Install required dependencies:**
   *(Ensure your terminal shows `(venv)` in your prompt before running this!)*
   ```bash
   pip install -r requirements.txt
   ```

## 5. Set Environment Variables
You must inject your API keys into your active terminal session. Choose ONE of the following methods depending on your key type:

### Setup A: Using Ed25519 / RSA Keys (Private Key File)
Save your Ed25519 or RSA private key text as a file named `private_key.pem` in the same folder.
* **Windows (PowerShell):**
  ```powershell
  $env:BINANCE_API_KEY="paste_api_key_here"
  $env:BINANCE_PRIVATE_KEY_PATH="private_key.pem"
  ```
* **Mac / Linux:**
  ```bash
  export BINANCE_API_KEY="paste_api_key_here"
  export BINANCE_PRIVATE_KEY_PATH="private_key.pem"
  ```

### Setup B: Using Standard HMAC Keys (Secret String)
* **Windows (PowerShell):**
  ```powershell
  $env:BINANCE_API_KEY="paste_api_key_here"
  $env:BINANCE_API_SECRET="paste_secret_key_here"
  ```
* **Mac / Linux:**
  ```bash
  export BINANCE_API_KEY="paste_api_key_here"
  export BINANCE_API_SECRET="paste_secret_key_here"
  ```

## 6. Running the Application
Ensure your terminal is in the root project folder, your `venv` is active, and your environment variables are set.

### Option A: Run the Visual GUI (Recommended)
```bash
python trading_bot/gui.py
```

### Option B: Run the Command Line Interface (CLI)

The CLI offers two ways to trade:

**1. Interactive Prompt (Easiest)**
Just run the command below, and the bot will ask you for all the necessary details like Symbol, Side, and Quantity step-by-step:
```bash
python trading_bot/cli.py trade
```

**2. Direct Command Syntax (For automation and fast execution)**
You can place orders instantly by passing all required arguments in a single line.

*   **Market Buy:** instantly buy 0.005 BTC at whatever the current market price is:
    ```bash
    python trading_bot/cli.py trade --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.005
    ```
*   **Limit Sell:** place an order to short (SELL) 0.02 ETH *only* if the price hits $3,500.00:
    ```bash
    python trading_bot/cli.py trade --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.02 --price 3500.0
    ```
*   **Short-hand flags:** (using `-s`, `-d`, `-t`, `-q`, `-p`):
    ```bash
    python trading_bot/cli.py trade -s BTCUSDT -d BUY -t LIMIT -q 0.01 -p 62000
    ```

For full documentation right in your terminal, run:
```bash
python trading_bot/cli.py --help
```
