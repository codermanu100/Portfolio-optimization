import numpy as np
import matplotlib.pyplot as plt
import Covariance_and_Correlation as cc
import Portfolio_return as pr

risk_free_rate = 0.01

def get_risk_matrix(folder_path,sector):
    
    expected_returns = np.array(pr.compute_expected_returns_vector(folder_path,sector))
    cov_matrix, corr_matrix= cc.compute_covariance_and_correlation(folder_path,sector)
    
    
    if expected_returns.ndim > 1:
        expected_returns = expected_returns.flatten()
    assert expected_returns.shape[0] == 5, "Expected 5 expected returns"

    def calculate_portfolio_variance(weights, cov_matrix):
        return np.dot(weights.T, np.dot(cov_matrix, weights))

    def generate_random_portfolio(cov_matrix, expected_returns):
        weights = np.random.random(len(expected_returns))
        weights /= np.sum(weights)
        variance = calculate_portfolio_variance(weights, cov_matrix)
        portfolio_return = np.dot(weights, expected_returns)
        volatility = np.sqrt(variance)
        sharpe_ratio = (portfolio_return - risk_free_rate) / volatility
        return weights, variance, portfolio_return, sharpe_ratio

    def efficient_frontier(cov_matrix, expected_returns, num_portfolios=10000):
        returns_list, volatilities_list, sharpe_list, weights_list = [], [], [], []

        for _ in range(num_portfolios):
            weights, variance, port_return, sharpe = generate_random_portfolio(cov_matrix, expected_returns)
            volatility = np.sqrt(variance)
            returns_list.append(port_return)
            volatilities_list.append(volatility)
            sharpe_list.append(sharpe)
            weights_list.append(weights)

        return np.array(returns_list), np.array(volatilities_list), np.array(sharpe_list), np.array(weights_list)

    returns_list, volatilities_list, sharpe_ratios, weights_list = efficient_frontier(cov_matrix, expected_returns)

    # Identify minimum risk and optimum risk portfolios
    min_vol_idx = np.argmin(volatilities_list)
    max_sharpe_idx = np.argmax(sharpe_ratios)
    

    # Plot Efficient Frontier
    plt.figure(figsize=(8,6))
    scatter = plt.scatter(volatilities_list, returns_list, c=sharpe_ratios, cmap='viridis', s=10)
    plt.colorbar(scatter, label='Sharpe Ratio')
    plt.title(f'Efficient Frontier with Minimum and Optimum Risk Portfolios: {sector}')
    plt.xlabel('Volatility (Risk)')
    plt.ylabel('Expected Return')

    # Minimum-risk portfolio (red star)
    plt.scatter(volatilities_list[min_vol_idx], returns_list[min_vol_idx],
                color='red', marker='*', s=200, label='Minimum Risk Portfolio')

    # Optimum-risk portfolio (green star)
    plt.scatter(volatilities_list[max_sharpe_idx], returns_list[max_sharpe_idx],
                color='green', marker='*', s=200, label='Optimum Risk Portfolio')

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    
    return returns_list, volatilities_list, sharpe_ratios, weights_list, min_vol_idx, max_sharpe_idx
    
    
