# src/analysis/visualization.py
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Any
import seaborn as sns  # Add this import
import logging

class TradingVisualizer:
    """Handles visualization of trading results"""
    
    def __init__(self, style: str = 'seaborn'):
        """
        Initialize visualizer with plotting style.
        
        Args:
            style: matplotlib style or 'seaborn' for seaborn style
        """
        self.logger = logging.getLogger(__name__)
        try:
            if style == 'seaborn':
                sns.set_theme(style='whitegrid')  # Use seaborn's styling
            else:
                plt.style.use(style)  # Use matplotlib's built-in styles
        except Exception as e:
            self.logger.warning(f"Could not set style {style}: {str(e)}")
            plt.style.use('default')

    def create_dashboard(self, price_data: pd.DataFrame, 
                       signals: Dict[str, Any],
                       metrics: Dict[str, float],
                       backtest: Dict[str, Any],
                       ticker: str) -> plt.Figure:
        """Create comprehensive trading dashboard"""
        fig, axes = plt.subplots(3, 1, figsize=(12, 12))
        
        # Price and signals plot
        self._plot_price_signals(axes[0], price_data, signals, ticker)
        
        # Returns plot
        self._plot_returns(axes[1], backtest['returns'], ticker)
        
        # Metrics table
        self._add_metrics_table(axes[2], metrics)
        
        fig.tight_layout()
        return fig

    def _plot_price_signals(self, ax, data: pd.DataFrame, signals: Dict[str, Any], ticker: str):
        """Plot price data with trading signals"""
        ax.plot(data['Close'], label='Price')
        
        # Plot buy signals
        buy_signals = signals['primary'] == 'BUY'
        if any(buy_signals):
            ax.plot(data.loc[buy_signals, 'Close'], '^', markersize=10, color='g', label='Buy')
        
        # Plot sell signals
        sell_signals = signals['primary'] == 'SELL'
        if any(sell_signals):
            ax.plot(data.loc[sell_signals, 'Close'], 'v', markersize=10, color='r', label='Sell')
        
        ax.set_title(f'{ticker} Price with Signals')
        ax.set_ylabel('Price')
        ax.legend()

    def _plot_returns(self, ax, returns: pd.Series, ticker: str):
        """Plot cumulative returns"""
        cumulative = (1 + returns).cumprod()
        ax.plot(cumulative)
        ax.set_title(f'{ticker} Cumulative Returns')
        ax.set_ylabel('Cumulative Return')
        ax.axhline(1, color='k', linestyle='--')

    def _add_metrics_table(self, ax, metrics: Dict[str, float]):
        """Add metrics table to plot"""
        # Convert metrics to display format
        display_metrics = {k: f"{v:.4f}" if isinstance(v, float) else str(v) 
                         for k, v in metrics.items()}
        
        # Create table
        table = ax.table(
            cellText=[[k, v] for k, v in display_metrics.items()],
            colLabels=['Metric', 'Value'],
            loc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        ax.axis('off')
        ax.set_title('Performance Metrics')

    def save_report(self, data: pd.DataFrame, metrics: Dict[str, float],
                   signals: Dict[str, Any], backtest: Dict[str, Any],
                   output_dir: str, ticker: str):
        """Save complete report to file"""
        fig = self.create_dashboard(data, signals, metrics, backtest, ticker)
        fig.savefig(f"{output_dir}/{ticker}_report.png")
        plt.close(fig)