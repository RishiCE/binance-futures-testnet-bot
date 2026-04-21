# Binance Futures Testnet Bot

This is a simplified trading bot for placing MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M). It includes both a clean CLI interface and a lightweight UI (`gui.py`) built with Tkinter.

## 1. Prerequisites
- **Python:** Python 3.8 to 3.12 is highly recommended. (Python 3.14 alpha has known compatibility issues with networking libraries).
- **Testnet Account:** A Binance Futures Testnet account.

## 2. API Key Generation
You can use either a standard **HMAC** key or a more secure **Ed25519 / RSA** key.
1. Go to the [Binance Futures Testnet](https://testnet.binancefuture.com/) site.
2. Click "Create API Key".
   * **For HMAC:** Choose "System Generated". Binance provides both the API Key and Secret Key. Copy them immediately before closing the window.
   * **For Ed25519 / RSA (Recommended):** Choose "Self-generated". **Note: Binance does NOT generate these for you.** You must use a local tool (like the official Binance Desktop Key Generator, OpenSSL, or ssh-keygen) to create a key pair. You then copy the **Public Key** and paste it into the Binance website. Store your **Private Key** text locally by saving it into a file named `private_key.pem` inside this project folder.

## 3. Local Setup & Environment (VS Code)
1. Extract the downloaded ZIP file and open the root folder in VS Code.
2. Open a new Terminal inside VS Code (`Ctrl + ` `).
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

## 4. Set Environment Variables
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

## 5. Running the Application
Ensure your terminal is in the root project folder, your `venv` is active, and your environment variables are set.

### Option A: Run the Visual GUI (Recommended)
```bash
python trading_bot/gui.py
```

### Option B: Run the Command Line Interface (CLI)
```bash
python trading_bot/cli.py --help
python trading_bot/cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.005
```
