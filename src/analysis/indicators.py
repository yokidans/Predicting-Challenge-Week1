import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class IndicatorConfig:
    """Configuration for technical indicators"""
    enabled: Dict[str, bool]
    parameters: Dict[str, Any]

class TechnicalIndicators:
    """Calculates various technical indicators"""
    
    def __init__(self, data: pd.DataFrame, config: IndicatorConfig):
        self.data = data.copy()
        self.config = config
    
    def calculate_enabled_indicators(self) -> pd.DataFrame:
        """Calculate all enabled indicators"""
        for indicator, enabled in self.config.enabled.items():
            if enabled:
                method_name = f'_calculate_{indicator}'
                if hasattr(self, method_name):
                    getattr(self, method_name)()
                else:
                    raise ValueError(f"No calculation method for {indicator}")
        return self.data
    
    def _calculate_rsi(self) -> None:
        """Calculate Relative Strength Index"""
        params = self.config.parameters['rsi']
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(params['period']).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(params['period']).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
    
    def _calculate_moving_averages(self) -> None:
        """Calculate moving averages"""
        params = self.config.parameters['moving_averages']
        self.data['MA_Short'] = self.data['Close'].rolling(params['short_window']).mean()
        self.data['MA_Long'] = self.data['Close'].rolling(params['long_window']).mean()
    
    def _calculate_bollinger_bands(self) -> None:
        """Calculate Bollinger Bands"""
        params = self.config.parameters['bollinger_bands']
        rolling_mean = self.data['Close'].rolling(params['window']).mean()
        rolling_std = self.data['Close'].rolling(params['window']).std()
        self.data['BB_Upper'] = rolling_mean + (rolling_std * params['std_dev'])
        self.data['BB_Lower'] = rolling_mean - (rolling_std * params['std_dev'])
    
    def _calculate_macd(self) -> None:
        """Calculate MACD"""
        params = self.config.parameters['macd']
        exp1 = self.data['Close'].ewm(span=params['fast_period'], adjust=False).mean()
        exp2 = self.data['Close'].ewm(span=params['slow_period'], adjust=False).mean()
        self.data['MACD'] = exp1 - exp2
        self.data['Signal_Line'] = self.data['MACD'].ewm(span=params['signal_period'], adjust=False).mean()