import os
import json
import numpy as np
import pandas as pd
import Minimum_risk_and_Optimum_risk as mro
import stock_list as sl
from sectors_list import sectors
from Dataset_Collection import collect_data, collect_data_for_stock

root="dataset"

def risk_report():
    with open("annual return report.txt","w") as f:
        f.write("Annual return report of every sector\n")
        
    with open("Covariance and Correlation report.txt","w") as f:
        f.write("Covariance and Correlation report of every sector\n")
        
    best_sector=["",""]
    max_optimum_risk_return=0
    max_minimum_risk_return=0
    optimum_vol=0
    minimum_vol=0
    optimum_risk_weight=[]
    minimum_risk_weight=[]
    with open("risk_report.txt", "w") as f:
        for sector in sectors:
            f.write(f"Sector: {sector}\n")
            folder_path = f"{root}/{sector}/"
            returns_list, volatilities_list, sharpe_ratios, weights_list, min_vol_idx, max_sharpe_idx = mro.get_risk_matrix(folder_path,sector)
            stock_list = sl.sectors[sector]

            def map_weights(index):
                return {stock: round(weight, 4) for stock, weight in zip(stock_list, weights_list[index])}

            min_vol_weights = map_weights(min_vol_idx)
            max_sharpe_weights = map_weights(max_sharpe_idx)

            
            f.write(" Minimum-Risk Portfolio:\n")
            f.write(f"  Return:      {returns_list[min_vol_idx]:.4f}\n")
            f.write(f"  Volatility:  {volatilities_list[min_vol_idx]:.4f}\n")
            f.write(f"  Sharpe Ratio:{sharpe_ratios[min_vol_idx]:.4f}\n")
            f.write(f"  Weights:     {json.dumps(min_vol_weights)}\n")

            f.write("\n Optimum-Risk Portfolio (Max Sharpe):\n")
            f.write(f"  Return:      {returns_list[max_sharpe_idx]:.4f}\n")
            f.write(f"  Volatility:  {volatilities_list[max_sharpe_idx]:.4f}\n")
            f.write(f"  Sharpe Ratio:{sharpe_ratios[max_sharpe_idx]:.4f}\n")
            f.write(f"  Weights:     {json.dumps(max_sharpe_weights)}\n")
            f.write("\n" + "="*100 + "\n\n")
            
            if(returns_list[max_sharpe_idx] > max_optimum_risk_return and sharpe_ratios[max_sharpe_idx]>1):
                max_optimum_risk_return=returns_list[max_sharpe_idx]
                best_sector[1]=sector
                optimum_risk_weight=max_sharpe_weights
                optimum_vol=volatilities_list[max_sharpe_idx]
            
            if(returns_list[min_vol_idx] > max_minimum_risk_return and sharpe_ratios[min_vol_idx]>1):
                max_minimum_risk_return=returns_list[min_vol_idx]
                best_sector[0]=sector  
                minimum_risk_weight=min_vol_weights
                minimum_vol=volatilities_list[min_vol_idx]
       
    return best_sector, minimum_risk_weight, optimum_risk_weight, max_optimum_risk_return, max_minimum_risk_return, minimum_vol, optimum_vol

