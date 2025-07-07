import numpy as np
import pandas as pd
from Finding_best_sector import risk_report

investment_duration = 0
investment_amount = 0
   
investment_duration = int(input("Enter your Investment Duration(in years):"))
investment_amount = int(input("Enter your Investment Amount(Min Rs.100):"))
    
print("Your Investment Duration(in years) is:", investment_duration)
print("Your Investment Amount is:", investment_amount)
print("\n")


best_sector, min_vol_weights, max_sharpe_weights, max_optimum_risk_return, max_minimum_risk_return, minimum_vol, optimum_vol=risk_report()

print("\nOptimum Risk Portfolio")
print("Best Sector", best_sector[1])
print(f"\nExpected Annual Return: {max_optimum_risk_return*100:.2f}%")
print(f"\nExpected Volatility: {optimum_vol*100:.2f}%")
print("\nStock \t Amount to Invest")
for stock, weight in max_sharpe_weights.items():
    print(f"{stock} \t {weight*investment_amount:.0f}")


print("\nMinimum Risk Portfolio")
print("Best Sector:", best_sector[0])
print(f"\nExpected Annual Return: {max_minimum_risk_return*100:.2f}%")
print(f"\nExpected Volatility: {minimum_vol*100:.2f}%")
print("\nStock \t Amount to Invest")
for stock, weight in min_vol_weights.items():
    print(f"{stock} \t {weight*investment_amount:.0f}")
    