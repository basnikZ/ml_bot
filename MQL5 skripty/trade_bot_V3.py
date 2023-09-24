import MetaTrader5 as mt5
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import time

ORDER_BUY = 0
ORDER_SELL = 1

def fetch_mt5_data(symbol, bars=1000):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, bars)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df[['close', 'tick_volume']]
    df.columns = ['Adj Close', 'Volume']
    return df

def prepare_data(df, lookback):
    features = ['Adj Close', 'Volume']
    dataset = df[features].copy()
    scalers = {}
    scaled_data = {}

    for feature in features:
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data[feature] = scaler.fit_transform(dataset[feature].values.reshape(-1, 1)).flatten()
        scalers[feature] = scaler

    dataset = pd.DataFrame(scaled_data)
    x_data, y_data = [], []

    for i in range(lookback, len(dataset)):
        x_data.append(dataset.iloc[i - lookback:i].values)
        y_data.append(dataset['Adj Close'].iloc[i])

    x_data, y_data = np.array(x_data), np.array(y_data)
    x_data = np.reshape(x_data, (x_data.shape[0], x_data.shape[1], len(features)))

    return x_data, y_data, scalers

def build_lstm_model(lookback, feature_count):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(lookback, feature_count)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def trading_decision(predicted_value, current_value):
    if predicted_value > current_value:
        return ORDER_BUY
    elif predicted_value < current_value:
        return ORDER_SELL
    else:
        return None

def place_order(action, symbol, volume):
    tick = mt5.symbol_info_tick(symbol)
    price = tick.ask if action == ORDER_BUY else tick.bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": action,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Python script order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
        return True
    else:
        print("Order failed, error:", mt5.last_error())
        return False

def main():
    if not mt5.initialize():
        print("MetaTrader5 initialization failed!")
        return

    print("MetaTrader5 initialized successfully!")

    symbol = "BTCUSD"
    volume = 0.01
    lookback = 24
    last_action = None

    while True:
        df = fetch_mt5_data(symbol, bars=1000)
        x_data, y_data, scalers = prepare_data(df, lookback)
        
        if len(x_data) < 2:
            print("Not enough data for training. Exiting.")
            return

        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, shuffle=False)
        model = build_lstm_model(lookback, x_data.shape[2])
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        model.fit(x_train, y_train, batch_size=1, epochs=10, validation_data=(x_test, y_test), callbacks=[early_stopping], verbose=0)

        print("Model retrained.")

        df_latest = fetch_mt5_data(symbol, bars=lookback+1)
        x_latest, _, _ = prepare_data(df_latest.tail(lookback+1), lookback)

        scaled_prediction = model.predict(x_latest[-1].reshape(1, lookback, 2))
        prediction = scalers['Adj Close'].inverse_transform(scaled_prediction)
        current_value = df['Adj Close'].iloc[-1]

        print(f"Prediction: {prediction[0][0]}, Current Value: {current_value}")

        action = trading_decision(prediction[0][0], current_value)

        if action is not None and action != last_action:
            if place_order(action, symbol, volume):
                print(f"Order {['BUY', 'SELL'][action]} executed at {current_value}")
                last_action = action

        time.sleep(30)

if __name__ == "__main__":
    main()
