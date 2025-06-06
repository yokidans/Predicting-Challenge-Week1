# News-Stock Correlation Analysis

## Overview
This Python script analyzes the correlation between news sentiment and stock price movements. It processes news headlines, calculates sentiment scores, and correlates them with daily stock returns.

## Features
- **Data Validation**: Robust path and data validation
- **Sentiment Analysis**: Uses TextBlob for polarity scoring
- **Statistical Correlation**: Pearson correlation calculation
- **Visualization**: Generates comparative plots
- **Error Handling**: Comprehensive exception handling

## Code Structure

### 1. Initialization (`__init__` method)
```python
def __init__(self, news_data_path: str, stock_data_path: str):
    """Initialize with path validation"""
    self.news_data_path = self._validate_path(news_data_path, "News data")
    self.stock_data_path = self._validate_path(stock_data_path, "Stock data")
    # ... other initializations
