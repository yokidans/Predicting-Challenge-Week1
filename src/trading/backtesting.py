# src/trading/backtesting.py
import pandas as pd
import numpy as np
from typing import Dict, Any
import logging
from src.analysis.metrics import FinancialMetrics  # Add this import

class Backtester:
    """
    Backtesting engine for trading strategies.
    Calculates performance metrics, position tracking, and risk management.
    """
    
    def __init__(self, prices: pd.Series, signals: pd.Series, config: Dict[str, Any]):
        """
        Initialize backtester with price data, signals, and configuration.
        
        Args:
            prices: Series of asset prices
            signals: Series of trading signals (BUY/SELL/NEUTRAL)
            config: Dictionary of backtesting parameters
        """
        self.prices = prices
        self.signals = signals
        self.config = {
            'initial_capital': 100000,
            'commission': 0.001,  # 0.1% commission
            'risk_free_rate': 0.02,
            'stop_loss': 0.05,    # 5% stop loss
            'take_profit': 0.10,  # 10% take profit
            **config  # Override defaults with provided config
        }
        self.logger = logging.getLogger(__name__)
               
    def run(self) -> Dict[str, Any]:
        """
        Run backtest and return comprehensive results.
        
        Returns:
            Dictionary containing:
            - returns: Series of strategy returns
            - positions: Series of positions
            - trades: DataFrame of trade records
            - metrics: Dictionary of performance metrics
        """
        self._validate_inputs()
        positions = self._generate_positions()
        returns = self._calculate_returns(positions)
        trades = self._generate_trade_history(positions)
        
        return {
            'returns': returns,
            'positions': positions,
            'trades': trades,
            'metrics': self._calculate_performance_metrics(returns)
        }
    
    def _validate_inputs(self) -> None:
        """Validate input data and signals"""
        if len(self.prices) != len(self.signals):
            raise ValueError("Prices and signals must have same length")
        
        if not isinstance(self.prices.index, pd.DatetimeIndex):
            raise ValueError("Prices must have datetime index")
            
        if not all(s in ['BUY', 'SELL', 'NEUTRAL'] for s in self.signals.unique()):
            raise ValueError("Signals must be BUY/SELL/NEUTRAL")
    
    def _generate_positions(self) -> pd.Series:
        """Generate position series from signals"""
        positions = pd.Series(0, index=self.prices.index)
        position = 0  # Current position (1=long, -1=short, 0=neutral)
        
        for i, (date, signal) in enumerate(self.signals.items()):
            if signal == 'BUY' and position <= 0:
                positions.iloc[i] = 1
                position = 1
            elif signal == 'SELL' and position >= 0:
                positions.iloc[i] = -1
                position = -1
            else:
                positions.iloc[i] = position
                
        return positions
    
    def _calculate_returns(self, positions: pd.Series) -> pd.Series:
        """Calculate strategy returns including commissions"""
        price_returns = self.prices.pct_change()
        strategy_returns = positions.shift(1) * price_returns
        
        # Apply commissions on position changes
        position_changes = positions.diff().abs()
        commissions = position_changes * self.config['commission']
        strategy_returns -= commissions
        
        return strategy_returns.dropna()
    
    def _generate_trade_history(self, positions: pd.Series) -> pd.DataFrame:
        """Generate detailed trade history"""
        trades = []
        position = 0
        entry_price = None
        entry_date = None
        
        for date, pos in positions.items():
            if pos != position:  # Position changed
                if position != 0:  # Exit previous position
                    exit_price = self.prices[date]
                    pct_change = (exit_price - entry_price) / entry_price * position
                    trades.append({
                        'entry_date': entry_date,
                        'exit_date': date,
                        'position': position,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'return': pct_change,
                        'duration': (date - entry_date).days
                    })
                
                if pos != 0:  # Enter new position
                    entry_price = self.prices[date]
                    entry_date = date
                
                position = pos
        
        return pd.DataFrame(trades)
    
    def _calculate_performance_metrics(self, returns: pd.Series) -> Dict[str, float]:
        """Calculate performance metrics from returns"""
        metrics = FinancialMetrics(returns, self.config['risk_free_rate'])
        return metrics.calculate_all()