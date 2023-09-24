import MetaTrader5 as mt5
import time

ORDER_BUY = 0
ORDER_SELL = 1

def place_order(action, symbol, volume):
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
    
    result = mt5.order_send(request)
    
    if not result or result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed, retcode={result.retcode if result else 'Unknown'}")
        print("Last error:", mt5.last_error())
    else:
        print(f"Order succeeded, deal={result.deal}")

def main():
    if not mt5.initialize():
        print("MetaTrader5 initialization failed!")
        return
    
    print("MetaTrader5 initialized successfully!")

    symbol = "BTCUSD"
    volume = 0.01

    print("Sending a BUY order...")
    place_order(ORDER_BUY, symbol, volume)
    
    time.sleep(2)  # 2 seconds delay
    
    print("Sending a SELL order...")
    place_order(ORDER_SELL, symbol, volume)
    
    mt5.shutdown()

if __name__ == "__main__":
    main()
