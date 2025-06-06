# Stock Trading Analysis Toolkit

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A professional-grade toolkit for multi-stock technical analysis, performance benchmarking, and trading system development.

## Key Features

### 📊 Professional Data Pipeline
- **Dual-source data loading**  
  - Automatic fallback between Yahoo Finance API and PyNance
  - Local caching in CSV/Parquet formats
  - Supports 1m, 5m, 15m, 1h, 1d timeframes
- **Data Quality Assurance**  
  - Automatic gap filling for missing periods
  - OHLCV validation checks
  - Corporate action adjustment (splits/dividends)

### 📈 Comprehensive Technical Analysis
- **TA-Lib Indicators (20+)**  
  ```python
  # Example indicator configuration
  from talib import RSI, MACD
  df['RSI_14'] = RSI(df['Close'], timeperiod=14)
  df['MACD'], _, _ = MACD(df['Close'])
  Trading System Ready
Signal Generation

python
# Weighted signal example
signals = (0.4*df['RSI_signal'] + 
          0.3*df['MACD_signal'] + 
          0.3*df['Volume_signal'])
Backtesting Framework

Slippage modeling (0.1-0.5% configurable)

Commission-aware returns

Benchmark-relative performance

📤 Production Outputs
bash
# Batch processing example
python analyze.py --tickers META AMZN GOOG --period 5y --output report.xlsx
Report Includes:

Performance tear sheet

Risk metrics table

Equity curve visualization

Position log (CSV)

Installation
bash
pip install -r requirements.txt
# Includes:
# yfinance>=0.2.18
# TA-Lib>=0.4.24
# mplfinance>=0.12.9b7
Usage
python
from toolkit import StockAnalyzer

analyzer = StockAnalyzer(tickers=['META', 'AMZN'], period='1y')
report = analyzer.generate_report()
report.save_excel('tech_stocks.xlsx')
Data Dictionary
Column	Description	Sample Values
SMA_20	20-day Simple MA	152.43
RSI_14	14-day RSI	67.2 (Overbought)
MACD_Hist	MACD Histogram	1.2 (Bullish)
License
MIT License - Free for commercial and academic use with attribution.
