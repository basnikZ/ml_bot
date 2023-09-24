import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping

def fetch_stock_data(ticker, start, end):
    stock_data = yf.download(ticker, start=start, end=end)
    return stock_data

def prepare_data(stock_data, lookback):
    data = stock_data.filter(['Adj Close'])
    dataset = data.values
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    x_data = []
    y_data = []

    for i in range(lookback, len(scaled_data)):
        x_data.append(scaled_data[i-lookback:i, 0])
        y_data.append(scaled_data[i, 0])

    x_data, y_data = np.array(x_data), np.array(y_data)
    x_data = np.reshape(x_data, (x_data.shape[0], x_data.shape[1], 1))

    return x_data, y_data, scaler

def build_lstm_model(lookback):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(lookback, 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def run_prediction(ticker, start, end):
    lookback = 60
    stock_data = fetch_stock_data(ticker, start, end)
    x_data, y_data, scaler = prepare_data(stock_data, lookback)
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, shuffle=False)
    model = build_lstm_model(lookback)
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    model.fit(x_train, y_train, batch_size=1, epochs=10, validation_data=(x_test, y_test), callbacks=[early_stopping])

    test_data = stock_data[-lookback-5:].filter(['Adj Close']).values
    test_data = scaler.transform(test_data)
    
    x_test = []
    for i in range(lookback, lookback+5):
        x_test.append(test_data[i-lookback:i, 0])
        
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    forecast = []
    for i, prediction in enumerate(predictions, 1):
        forecast.append((i, prediction[0]))
    
    return forecast
