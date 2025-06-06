import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum, auto

class SignalType(Enum):
    """Enumeration of possible signal types"""
    NEUTRAL = auto()
    BUY = auto()
    SELL = auto()
    STRONG_BUY = auto()
    STRONG_SELL = auto()

    @property
    def simple_name(self):
        """Convert to simple string representation"""
        return {
            SignalType.NEUTRAL: 'NEUTRAL',
            SignalType.BUY: 'BUY',
            SignalType.SELL: 'SELL',
            SignalType.STRONG_BUY: 'BUY',
            SignalType.STRONG_SELL: 'SELL'
        }[self]
@dataclass
class SignalConfig:
    """Configuration for signal generation with validation"""
    enabled: Dict[str, bool]
    parameters: Dict[str, Dict[str, Any]]
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        self.validate()
    
    def validate(self):
        """Validate all parameters"""
        # Validate enabled signals
        if not isinstance(self.enabled, dict):
            raise ValueError("Enabled signals must be a dictionary")
            
        # Validate parameters
        if not isinstance(self.parameters, dict):
            raise ValueError("Parameters must be a dictionary")
            
        # Validate each parameter group
        for signal_name, params in self.parameters.items():
            if not isinstance(params, dict):
                raise ValueError(f"Parameters for {signal_name} must be a dictionary")
            
            # Signal-specific validation
            if signal_name == 'rsi':
                if not (10 <= params.get('period', 14) <= 30):
                    raise ValueError("RSI period must be between 10 and 30")
                if not (60 <= params.get('overbought', 70) <= 80):
                    raise ValueError("RSI overbought must be between 60 and 80")
                if not (20 <= params.get('oversold', 30) <= 40):
                    raise ValueError("RSI oversold must be between 20 and 40")
            
            elif signal_name == 'macd':
                if not (8 <= params.get('fast_period', 12) <= 26):
                    raise ValueError("MACD fast period must be between 8 and 26")
                if not (12 <= params.get('slow_period', 26) <= 50):
                    raise ValueError("MACD slow period must be between 12 and 50")
                if not (5 <= params.get('signal_period', 9) <= 20):
                    raise ValueError("MACD signal period must be between 5 and 20")
            
            elif signal_name == 'moving_average':
                if not (5 <= params.get('short_window', 20) <= 50):
                    raise ValueError("MA short window must be between 5 and 50")
                if not (20 <= params.get('long_window', 50) <= 200):
                    raise ValueError("MA long window must be between 20 and 200")
            
            elif signal_name == 'bollinger':
                if not (10 <= params.get('window', 20) <= 50):
                    raise ValueError("Bollinger window must be between 10 and 50")
                if not (1.5 <= params.get('std_dev', 2.0) <= 3.0):
                    raise ValueError("Bollinger std_dev must be between 1.5 and 3.0")

class SignalGenerator:
    """
    Advanced trading signal generator with multiple technical indicators
    and risk management features.
    """
    
    def __init__(self, ohlc_data: pd.DataFrame, config: SignalConfig):
        """
        Initialize with OHLC data and configuration.
        
        Args:
            ohlc_data: DataFrame with Open, High, Low, Close columns
            config: SignalConfig object with parameters
        """
        self.data = ohlc_data.copy()
        self.config = config
        self._precompute_indicators()
    
    def _precompute_indicators(self) -> None:
        """Precompute all technical indicators needed for signals"""
        # RSI
        if self.config.enabled.get('rsi', False):
            params = self.config.parameters['rsi']
            delta = self.data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(params['period']).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(params['period']).mean()
            rs = gain / loss
            self.data['RSI'] = 100 - (100 / (1 + rs))
        
        # Moving Averages
        if self.config.enabled.get('moving_average', False):
            params = self.config.parameters['moving_average']
            self.data['MA_Short'] = self.data['Close'].rolling(params['short_window']).mean()
            self.data['MA_Long'] = self.data['Close'].rolling(params['long_window']).mean()
        
        # Bollinger Bands
        if self.config.enabled.get('bollinger', False):
            params = self.config.parameters['bollinger']
            rolling_mean = self.data['Close'].rolling(params['window']).mean()
            rolling_std = self.data['Close'].rolling(params['window']).std()
            self.data['BB_Upper'] = rolling_mean + (rolling_std * params['std_dev'])
            self.data['BB_Lower'] = rolling_mean - (rolling_std * params['std_dev'])
        
        # MACD
        if self.config.enabled.get('macd', False):
            params = self.config.parameters['macd']
            exp1 = self.data['Close'].ewm(span=params['fast_period'], adjust=False).mean()
            exp2 = self.data['Close'].ewm(span=params['slow_period'], adjust=False).mean()
            self.data['MACD'] = exp1 - exp2
            self.data['Signal_Line'] = self.data['MACD'].ewm(span=params['signal_period'], adjust=False).mean()
    
    def generate_signals(self) -> pd.Series:
        """
        Generate comprehensive trading signals based on multiple indicators.
        
        Returns:
            Series of SignalType enum values
        """
        signals = pd.Series(SignalType.NEUTRAL, index=self.data.index, name='Signal')
        
        # Initialize conditions
        ma_cross_above = False
        ma_cross_below = False
        rsi_overbought = False
        rsi_oversold = False
        price_below_bb_lower = False
        price_above_bb_upper = False
        macd_above_signal = False
        macd_below_signal = False
        
        # Calculate conditions only for enabled indicators
        if self.config.enabled.get('moving_average', False):
            ma_cross_above = (self.data['MA_Short'] > self.data['MA_Long']) & \
                           (self.data['MA_Short'].shift(1) <= self.data['MA_Long'].shift(1))
            ma_cross_below = (self.data['MA_Short'] < self.data['MA_Long']) & \
                           (self.data['MA_Short'].shift(1) >= self.data['MA_Long'].shift(1))
        
        if self.config.enabled.get('rsi', False):
            params = self.config.parameters['rsi']
            rsi_overbought = self.data['RSI'] > params['overbought']
            rsi_oversold = self.data['RSI'] < params['oversold']
        
        if self.config.enabled.get('bollinger', False):
            price_below_bb_lower = self.data['Close'] < self.data['BB_Lower']
            price_above_bb_upper = self.data['Close'] > self.data['BB_Upper']
        
        if self.config.enabled.get('macd', False):
            macd_above_signal = (self.data['MACD'] > self.data['Signal_Line']) & \
                              (self.data['MACD'].shift(1) <= self.data['Signal_Line'].shift(1))
            macd_below_signal = (self.data['MACD'] < self.data['Signal_Line']) & \
                              (self.data['MACD'].shift(1) >= self.data['Signal_Line'].shift(1))
        
        # Combined signals
        strong_buy = ma_cross_above & rsi_oversold & price_below_bb_lower & macd_above_signal
        strong_sell = ma_cross_below & rsi_overbought & price_above_bb_upper & macd_below_signal
        buy = ma_cross_above | macd_above_signal
        sell = ma_cross_below | macd_below_signal
        
        signals.loc[strong_buy] = SignalType.STRONG_BUY
        signals.loc[strong_sell] = SignalType.STRONG_SELL
        signals.loc[buy & ~strong_buy] = SignalType.BUY
        signals.loc[sell & ~strong_sell] = SignalType.SELL
        
        return signals
    
    def generate_all_signals(self) -> Dict[str, Any]:
        """
        Generate all signals and return as dictionary.
        Main entry point for the signal generation pipeline.
        """
        return {
            'primary': self.generate_signals(),
            'metadata': {
                'config': {
                    'enabled': self.config.enabled,
                    'parameters': self.config.parameters
                },
                'indicators': list(self.data.columns)
            }
        }