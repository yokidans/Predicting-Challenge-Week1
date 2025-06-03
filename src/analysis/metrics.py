# src/analysis/metrics.py
import numpy as np
import pandas as pd
from typing import Dict, Any
import logging

class FinancialMetrics:
    """
    Calculates various financial performance metrics from return series.
    Includes risk-adjusted returns, drawdown metrics, and performance ratios.
    """
    
    def __init__(self, returns: pd.Series, risk_free_rate: float = 0.02):
        """
        Initialize with return series and optional risk-free rate.
        
        Args:
            returns: Pandas Series of asset returns
            risk_free_rate: Annualized risk-free rate (default 2%)
        """
        self.returns = returns.dropna()
        self.risk_free_rate = risk_free_rate
        self.logger = logging.getLogger(__name__)
        
    def calculate_all(self) -> Dict[str, float]:
        """
        Calculate and return all available metrics.
        
        Returns:
            Dictionary of metric names and values
        """
        return {
            'total_return': self.total_return(),
            'annualized_return': self.annualized_return(),
            'annualized_volatility': self.annualized_volatility(),
            'sharpe_ratio': self.sharpe_ratio(),
            'sortino_ratio': self.sortino_ratio(),
            'max_drawdown': self.max_drawdown(),
            'calmar_ratio': self.calmar_ratio(),
            'win_rate': self.win_rate(),
            'profit_factor': self.profit_factor(),
            'skewness': self.skewness(),
            'kurtosis': self.kurtosis()
        }
    
    def total_return(self) -> float:
        """Calculate cumulative return for entire period"""
        return (1 + self.returns).prod() - 1
    
    def annualized_return(self, periods_per_year: int = 252) -> float:
        """Calculate annualized return"""
        return (1 + self.returns.mean())**periods_per_year - 1
    
    def annualized_volatility(self, periods_per_year: int = 252) -> float:
        """Calculate annualized volatility"""
        return self.returns.std() * np.sqrt(periods_per_year)
    
    def sharpe_ratio(self, periods_per_year: int = 252) -> float:
        """Calculate annualized Sharpe ratio"""
        excess_returns = self.returns - (self.risk_free_rate / periods_per_year)
        return excess_returns.mean() / excess_returns.std() * np.sqrt(periods_per_year)
    
    def sortino_ratio(self, periods_per_year: int = 252) -> float:
        """Calculate annualized Sortino ratio"""
        downside_returns = self.returns[self.returns < 0]
        if len(downside_returns) == 0:
            return np.nan
        downside_std = downside_returns.std()
        excess_returns = self.returns - (self.risk_free_rate / periods_per_year)
        return excess_returns.mean() / downside_std * np.sqrt(periods_per_year)
    
    def max_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        cumulative = (1 + self.returns).cumprod()
        peak = cumulative.expanding(min_periods=1).max()
        drawdown = (cumulative - peak) / peak
        return drawdown.min()
    
    def calmar_ratio(self, periods_per_year: int = 252) -> float:
        """Calculate Calmar ratio (annualized return / max drawdown)"""
        max_dd = abs(self.max_drawdown())
        if max_dd == 0:
            return np.nan
        return self.annualized_return(periods_per_year) / max_dd
    
    def win_rate(self) -> float:
        """Calculate percentage of positive return periods"""
        return (self.returns > 0).mean()
    
    def profit_factor(self) -> float:
        """Calculate profit factor (gross profits / gross losses)"""
        gross_profits = self.returns[self.returns > 0].sum()
        gross_losses = abs(self.returns[self.returns < 0].sum())
        if gross_losses == 0:
            return np.inf
        return gross_profits / gross_losses
    
    def skewness(self) -> float:
        """Calculate return distribution skewness"""
        return self.returns.skew()
    
    def kurtosis(self) -> float:
        """Calculate return distribution kurtosis"""
        return self.returns.kurtosis()