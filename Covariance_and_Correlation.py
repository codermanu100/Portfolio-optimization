import os
import pandas as pd
import numpy as np


def compute_covariance_and_correlation(folder_path,sector):
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

            if df.index.duplicated().any():
                print(f"Duplicate dates found in {stock_name}. Removing duplicates.")
                df = df[~df.index.duplicated(keep='first')]

            if df.empty:
                print(f"Skipping {stock_name} — empty after return calc.")
                continue

            returns_dict[stock_name] = df['Daily Return']

    returns_df = pd.DataFrame(returns_dict)

    returns_df = returns_df.dropna()
    cov_matrix = returns_df.cov()
    corr_matrix = returns_df.corr()

    # Storing Covariance and Correlation report
    with open("Covariance and Correlation report.txt", "a") as f:
        f.write(f'{sector}\n')
        f.write("Covariance Matrix:\n")
        f.write(str(cov_matrix))
        f.write("\n\n")
        f.write("Correlation Matrix:\n")
        f.write(str(returns_df.corr()))
        f.write("\n\n" + "="*100 + "\n\n")
        
    return cov_matrix, corr_matrix
