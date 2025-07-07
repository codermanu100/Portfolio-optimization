import numpy as np
import os
import pandas as pd
from sectors_list import sectors

def clear_rough_data():
    for sector in sectors:
        folder_path=f"dataset/{sector}"
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                filepath = os.path.join(folder_path, filename)
                stock_name = filename.replace(".csv", "")
                df = pd.read_csv(filepath, parse_dates=True, index_col=0)
                df = df.drop(df.index[0])
                df = df.dropna()
                df = df.dropna(subset=['Open'])
                df.to_csv(filepath, index=False)