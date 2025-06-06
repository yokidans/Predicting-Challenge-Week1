# src/data/loader.py
import pandas as pd
from pathlib import Path
from typing import Optional
import logging

class FinancialDataLoader:
    """Loads financial data from various sources"""
    
    def __init__(self, data_dir: str = 'data/raw'):
        self.data_dir = Path(data_dir)
        self.logger = logging.getLogger(__name__)
        
    def load_from_csv(self, ticker: str) -> pd.DataFrame:
        """Load data from CSV file"""
        file_path = self.data_dir / f"{ticker}.csv"
        self.logger.debug(f"Loading data from {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
            
        try:
            data = pd.read_csv(
                file_path,
                parse_dates=['Date'],
                index_col='Date'
            )
            # Ensure standard column names
            data.columns = data.columns.str.capitalize()
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to load {ticker} data: {str(e)}")
            raise
            
      