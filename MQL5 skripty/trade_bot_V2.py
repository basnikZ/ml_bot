import MetaTrader5 as mt5
import time

ORDER_BUY = 0
ORDER_SELL = 1

def place_order(action, symbol, volume, order_ticket=None):
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print("Failed to retrieve the tick data")
        return
        
    price = tick.ask if action == ORDER_BUY else tick.bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": ORDER_BUY if action == ORDER_BUY else ORDER_SELL,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Python script order",
        "type_time": mt5.ORDER_TIME_GTC,  # Good till cancelled
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # If order_ticket is provided, it means we are closing an existing trade
    if order_ticket is not None:
        request["position"] = order_ticket

    result = mt5.order_send(request)
    
    if not result or result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed, retcode={result.retcode if result else 'Unknown'}")
        print("Last error:", mt5.last_error())
        return None
    else:
        print(f"Order succeeded, deal={result.deal}")
        return result.order  # Return the order ticket for future reference

def main():
    if not mt5.initialize():
        print("MetaTrader5 initialization failed!")
        return
    
    print("MetaTrader5 initialized successfully!")

    symbol = "BTCUSD"
    volume = 0.01

    try:
        while True:
            print("Sending a BUY order...")
            order_ticket = place_order(ORDER_BUY, symbol, volume)

            if order_ticket is not None:
                time.sleep(15)  # 15 seconds delay

                print("Closing the BUY order...")
                place_order(ORDER_SELL, symbol, volume, order_ticket)

            time.sleep(15)  # 15 seconds delay before starting the next cycle
    except KeyboardInterrupt:
        print("Script interrupted by user.")
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    main()


