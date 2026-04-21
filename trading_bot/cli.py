import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import typer
from rich.console import Console
from bot.validators import validate_symbol, validate_order_type, validate_side
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager

# Typer handles standard CLI capabilities intuitively
app = typer.Typer(help="Simplified Binance Futures Testnet Trading Bot")
console = Console()

@app.command()
def trade(
    symbol: str = typer.Option(..., "--symbol", "-s", prompt=True, help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", prompt=True, help="Order side: BUY or SELL"),
    order_type: str = typer.Option("MARKET", "--order-type", "-t", prompt="Order Type (MARKET/LIMIT)", help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Option(..., "--quantity", "-q", prompt=True, help="Amount to trade (e.g., 0.001)"),
    price: float = typer.Option(None, "--price", "-p", help="Price per unit (Required for LIMIT order)")
):
    """
    Place a MARKET or LIMIT order on Binance Futures Testnet.
    """
    console.print(f"\n[bold cyan]Starting Binance Futures Trading Bot...[/bold cyan]")

    try:
        # Cross-field and value validations
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type, price)

        # Dynamic prompting if LIMIT price is missing
        if order_type == "LIMIT" and price is None:
            price = float(typer.prompt("Please enter the LIMIT price"))

        # Initialize API client
        client_wrapper = BinanceFuturesClient()
        manager = OrderManager(client_wrapper)

        # Execution
        console.print(f"[yellow]Sending {order_type} {side} order for {quantity} {symbol}...[/yellow]")
        result = manager.place_order(symbol, side, order_type, quantity, price)

        # Clean Console Output
        if result:
            console.print("\n[bold green]✅ Order Placed Successfully![/bold green]")
            console.print(f"  Order ID:     [bold]{result.get('orderId')}[/bold]")
            console.print(f"  Status:       [bold]{result.get('status')}[/bold]")
            console.print(f"  Executed Qty: {result.get('executedQty')}")
            if result.get('avgPrice') and result.get('avgPrice') != "0.00000":
                console.print(f"  Avg Exec Prc: {result.get('avgPrice')}")
            console.print("\n[dim]View trading_bot.log for detailed JSON responses.[/dim]\n")
        else:
            console.print("[bold red]❌ Order Failed. Please check the logs.[/bold red]")

    except ValueError as ve:
        console.print(f"\n[bold red]Validation Error:[/bold red] {ve}")
    except EnvironmentError as ee:
        console.print(f"\n[bold red]Configuration Error:[/bold red] {ee}")
    except Exception as e:
        console.print(f"\n[bold red]System Error:[/bold red] {e}")


if __name__ == "__main__":
    app()
