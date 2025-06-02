
# Quantitative Financial Analysis with TA-Lib and PyNance

This Task-2 branch performs quantitative financial analysis on stock market data using TA-Lib for technical indicators and PyNance for financial metrics. The goal is to derive actionable insights from price and volume data to support trading and investment decisions.


## Project Overview

### 1. Key Tasks
1.Data Loading & Preparation:
  -Compute moving averages (SMA, EMA) to identify trends.
  -Calculate Relative Strength Index (RSI) for overbought/oversold conditions.
  -Generate MACD (Moving Average Convergence Divergence) signals for momentum analysis.
  -Apply Bollinger Bands to assess volatility and price reversals.
2.Technical Analysis with TA-Lib
  -Compute volatility measures (standard deviation, historical volatility).
  -Evaluate risk-adjusted returns using the Sharpe Ratio.
  -Calculate maximum drawdown to assess downside risk.
  -Analyze liquidity and volume trends for market participation insights.
3.Financial Metrics with PyNance
  - Publication frequency trends
  - News spike detection
  - Publishing time patterns
4.Visualizations:
  - Price and volume charts
  - Technical indicator plots
  - Performance metric graphs

## Expected Outputs
-✅ Technical Indicators Visualization
   -Price charts with moving averages & Bollinger Bands
   -RSI and MACD signals for trade setups

-✅ Financial Metrics Summary
    -Annualized volatility and Sharpe Ratio
    -Maximum drawdown analysis

-✅ Actionable Insights
    -Trend confirmation using moving averages
    -Overbought/oversold signals from RSI
    -Momentum shifts from MACD crossovers
=======
## Dependencies
  -Python 3.8+
  -Libraries:
  -pandas (Data manipulation)
  -numpy (Numerical computations)
  -matplotlib/seaborn (Visualizations)
  -TA-Lib (Technical indicators)
### jupyter notebook quantitative_analysis.ipynb
## Contributing
 Contributions are welcome! Open an Issue or Pull Request for improvements.
## License: MIT
