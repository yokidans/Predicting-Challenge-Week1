import pandas as pd
from typing import Dict

class DataProcessor:
    """Clean and process financial data"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def handle_missing_data(self) -> 'DataProcessor':
        """Handle missing values in the data"""
        self.data = self.data.dropna()
        return self
        
    def get_processed_data(self) -> pd.DataFrame:
        """Return the processed DataFrame"""
        return self.data