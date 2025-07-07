import os
import pandas as pd
import numpy as np
from sectors_list import sectors  

def compute_expected_returns_vector(folder_path,sector):
    returns_dict = {}

    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            stock_name = file.replace('.csv', '')
            file_path = os.path.join(folder_path, file)

            df = pd.read_csv(file_path)
            if 'Open' not in df.columns:
                print(f"Skipping {stock_name} — 'Open' not found.")
                continue

            df['Daily Return'] = df['Open'].pct_change()
            df = df.dropna(subset=['Daily Return'])

            if df.empty:
                print(f"Skipping {stock_name} — no data after return calc.")
                continue

            returns_dict[stock_name] = df['Daily Return']

    returns_df = pd.DataFrame(returns_dict).dropna()
    if returns_df.empty:
        print("No common date range or valid data.")
        return None

    mean_daily_returns = returns_df.mean()
    annual_returns = mean_daily_returns * 252  
            
    with open("annual return report.txt", "a") as f:
        f.write(f'{sector}\n')
        f.write("Expected Annual Returns:\n")
        for stock, ret in annual_returns.items():
            f.write(f"{stock}: {ret:.4f}\n")
        f.write("\n\n" + "="*100 + "\n\n")
    
    return annual_returns.to_numpy()  
