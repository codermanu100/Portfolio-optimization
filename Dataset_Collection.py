import yfinance as yf
import pandas as pd
from stock_list import sectors
from datetime import datetime, timedelta
from Dataset_Clearing_row import clear_rough_data

now=datetime.now()

def collect_data():
    start_date = "2021-01-01"
    end_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    
    for sector, stocks in sectors.items():
        sector_data = {}
        for stock in stocks:
            stock_data = yf.download(stock, start=start_date, end=end_date, progress=False)
            if(not stock_data.empty):
                stock_data.to_csv(f"dataset/{sector}/{stock}.csv",index=False)
            else:
                print(f"Skipped: {stock} - No data available")
    
    clear_rough_data()
    print("Data collection completed.")


def collect_data_for_stock(ticker="^NSEI", start_date="2021-01-01", end_date=(now - timedelta(days=1)).strftime("%Y-%m-%d")):
    
    stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if(not stock_data.empty):
        return stock_data
    else:
        print(f"Skipped: {ticker} - No data available")