import tkinter as tk
from stock_predictor import run_prediction

def fetch_forecast():
    ticker = ticker_entry.get()
    start = start_entry.get()
    end = end_entry.get()
    
    forecast = run_prediction(ticker, start, end)
    forecast_text = "\n".join([f"Day {day}: {price}" for day, price in forecast])
    
    forecast_label.config(text=forecast_text)

app = tk.Tk()
app.title("Stock Price Predictor")

# Create input fields and labels
ticker_label = tk.Label(app, text="Ticker")
ticker_label.pack()
ticker_entry = tk.Entry(app)
ticker_entry.pack()

start_label = tk.Label(app, text="Start Date (YYYY-MM-DD)")
start_label.pack()
start_entry = tk.Entry(app)
start_entry.pack()

end_label = tk.Label(app, text="End Date (YYYY-MM-DD)")
end_label.pack()
end_entry = tk.Entry(app)
end_entry.pack()

# Create the button and forecast label
btn = tk.Button(app, text="Fetch Forecast", command=fetch_forecast)
btn.pack()

forecast_label = tk.Label(app, text="")
forecast_label.pack()

app.mainloop()
