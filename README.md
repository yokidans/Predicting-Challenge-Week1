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
     python
    def __init__(self, news_data_path: str, stock_data_path: str):
    """Initialize with path validation"""
    self.news_data_path = self._validate_path(news_data_path, "News data")
    self.stock_data_path = self._validate_path(stock_data_path, "Stock data")
    # ... other initializations

- Validates input file paths

- Initializes data storage attributes

- Prints initialization confirmation

## 2. Data Loading (load_data method)
python
def load_data(self) -> bool:
    # Loads CSV files with datetime parsing
    # Performs data quality checks
    # Calculates daily returns
### Key operations:

- Reads news and stock CSV files

- Converts date columns to datetime objects

- Validates required columns exist

- Calculates daily percentage returns

## 3. Sentiment Analysis (calculate_sentiment_scores method)
    python
    def calculate_sentiment_scores(self) -> pd.DataFrame:
    # Uses TextBlob for sentiment analysis
    # Aggregates scores by date and stock
- Processes each headline with TextBlob

- Calculates polarity scores (-1 to 1)

- Returns DataFrame with average sentiment scores

## 4. Correlation Analysis (analyze_correlations method)
    python
    def analyze_correlations(self) -> dict:
    # Merges news and stock data
    # Calculates Pearson correlations
- Joins sentiment and return data

- Computes correlation for each stock

- Handles cases with insufficient data

## 5. Visualization (plot_results method)
    python
    def plot_results(self, correlations: dict):
    # Creates two-panel visualization
### Output includes:

- Bar plot of correlation coefficients

- Scatter plot of sentiment vs returns

- Saves plot as PNG file

### Dependencies
- pandas

- numpy

- TextBlob

- scipy

- matplotlib

- seaborn

- tqdm

### Error Handling
The code includes comprehensive error checking for:

- Missing files

- Invalid data formats

- Date parsing issues

- Missing required columns

- Calculation errors

### Output
- Console output of correlation results

- Saved visualization (correlation_analysis.png)

- Progress feedback during processing
