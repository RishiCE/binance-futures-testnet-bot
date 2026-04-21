import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import validate_symbol, validate_side, validate_order_type

class TradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binance Testnet Bot GUI")
        self.root.geometry("400x500")

        # Connection Warning
        self.client_wrapper = None
        self.manager = None
        
        # UI Setup
        self.create_widgets()
        self.log_message("Initializing client...")
        threading.Thread(target=self.init_client, daemon=True).start()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Symbol
        ttk.Label(frame, text="Symbol:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.symbol_var = tk.StringVar(value="BTCUSDT")
        ttk.Entry(frame, textvariable=self.symbol_var).grid(row=0, column=1, pady=2, sticky=tk.EW)

        # Side
        ttk.Label(frame, text="Side:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.side_var = tk.StringVar(value="BUY")
        ttk.Combobox(frame, textvariable=self.side_var, values=["BUY", "SELL"], state="readonly").grid(row=1, column=1, pady=2, sticky=tk.EW)

        # Type
        ttk.Label(frame, text="Order Type:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.type_var = tk.StringVar(value="LIMIT")
        self.type_cb = ttk.Combobox(frame, textvariable=self.type_var, values=["LIMIT", "MARKET"], state="readonly")
        self.type_cb.grid(row=2, column=1, pady=2, sticky=tk.EW)
        self.type_cb.bind('<<ComboboxSelected>>', self.toggle_price)

        # Quantity
        ttk.Label(frame, text="Quantity:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.qty_var = tk.StringVar(value="0.005")
        ttk.Entry(frame, textvariable=self.qty_var).grid(row=3, column=1, pady=2, sticky=tk.EW)

        # Price
        ttk.Label(frame, text="Price:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.price_var = tk.StringVar(value="42150.0")
        self.price_entry = ttk.Entry(frame, textvariable=self.price_var)
        self.price_entry.grid(row=4, column=1, pady=2, sticky=tk.EW)

        # Place Order Button
        self.btn = ttk.Button(frame, text="PLACE ORDER", command=self.place_order)
        self.btn.grid(row=5, column=0, columnspan=2, pady=15, sticky=tk.EW)

        # Log Window
        ttk.Label(frame, text="Event Log:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.log_area = scrolledtext.ScrolledText(frame, height=12, state="disabled")
        self.log_area.grid(row=7, column=0, columnspan=2, sticky=tk.NSEW)
        frame.rowconfigure(7, weight=1)
        frame.columnconfigure(1, weight=1)

    def init_client(self):
        try:
            self.client_wrapper = BinanceFuturesClient()
            self.manager = OrderManager(self.client_wrapper)
            self.log_message("[SUCCESS] API Connected. Ready to trade.")
        except Exception as e:
            self.log_message(f"[ERROR] API Initialization failed: {e}")
            self.log_message("Please check BINANCE_API_KEY env variables.")

    def toggle_price(self, event=None):
        if self.type_var.get() == "MARKET":
            self.price_entry.state(['disabled'])
        else:
            self.price_entry.state(['!disabled'])

    def log_message(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def execute_trade_thread(self, symbol, side, order_type, qty, price):
        self.log_message(f"> Sending {order_type} {side} for {qty} {symbol}...")
        try:
            res = self.manager.place_order(symbol, side, order_type, qty, price)
            if res:
                self.log_message(f"[SUCCESS] Order Placed! ID: {res.get('orderId')}")
            else:
                self.log_message("[FAILED] Check trading_bot.log for detailed API errors.")
        except Exception as e:
            self.log_message(f"[ERROR] Engine exception: {e}")
        finally:
            self.btn.config(state="normal")

    def place_order(self):
        if not self.manager:
            messagebox.showerror("Error", "API client not initialized. Check Env Variables.")
            return

        try:
            symbol = validate_symbol(self.symbol_var.get())
            side = validate_side(self.side_var.get())
            qty = float(self.qty_var.get())
            
            p_val = float(self.price_var.get()) if self.price_var.get() else None
            order_type = validate_order_type(self.type_var.get(), p_val)

            self.btn.config(state="disabled")
            threading.Thread(
                target=self.execute_trade_thread, 
                args=(symbol, side, order_type, qty, p_val),
                daemon=True
            ).start()

        except ValueError as ve:
            messagebox.showwarning("Validation Error", str(ve))

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()
