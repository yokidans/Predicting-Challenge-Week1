# 1. Introduction
## Project Overview
This project conducts rigorous analysis of financial news sentiment and its correlation with stock price movements. Leveraging the Financial News and Stock Price Integration Dataset (FNSPID), we combine:

- Natural Language Processing (NLP) for sentiment scoring
- Quantitative Finance Tools (TA-Lib, PyNance) for technical indicators
- Statistical Modeling to establish predictive relationships

## Business Context
Nova Financial Solutions aims to:
✔ Develop AI-driven trading signals from news sentiment
✔ Quantify the impact of media tone on market movements
✔ Build a predictive framework for algorithmic trading

## Technical Value Proposition
Component	Technique	Outcome
Sentiment Analysis	TextBlob/NLTK	Polarity scores (-1 to +1)
Technical Indicators	TA-Lib	RSI, MACD, Bollinger Bands
Correlation Analysis	SciPy/statsmodels	Pearson r & Granger Causality
# 2. Project Documentation
## Dataset Specifications
## FNSPID Schema

Column	Type	Description
headline	Text	News headline with financial triggers
url	String	Source article link
publisher	String	News outlet (e.g., Bloomberg)
date	DateTime	UTC-4 timestamp
stock	String	Ticker symbol (e.g., AAPL)


# 3. Installation & Configuration
## System Requirements
- Python ≥3.8
- Git LFS (for large datasets)
- TA-Lib C library pre-installed

## Setup Guide
# 1. Clone repo with LFS support  
git lfs install  
git clone https://github.com/your-repo/Predicting-Challenge-Week1.git  

# 2. Configure environment  
python -m venv .venv && source .venv/bin/activate  # Unix  
.venv\Scripts\activate                              # Windows  

# 3. Install dependencies  
pip install -r requirements.txt  
Critical Dependencies
 
pandas>=2.0, numpy>=1.24, scipy>=1.10  
textblob>=0.17.1, nltk>=3.8  
ta-lib==0.4.24, pynance>=1.2, yfinance>=0.2.18  
matplotlib>=3.7, seaborn>=0.12  

## Folder Architecture
markdown
├── data/  
│   ├── raw/               # Original FNSPID  
│   └── processed/         # Cleaned datasets  
├── docs/                  # Reports & presentations  
├── notebooks/  
│   ├── EDA.ipynb          # Exploratory analysis  
│   └── Modeling.ipynb     # Correlation studies  
├── src/  
│   ├── data_pipeline.py   # ETL workflows  
│   ├── sentiment.py       # NLP processing  
│   └── finance.py         # TA-Lib wrappers  
└── tests/                 # Pytest units  
# 4. Feedback & Quality Assurance
Identified Defects & Solutions
Issue	Root Cause	Resolution
Timezone conflicts	Mixed UTC-4/UTC timestamps	Normalized to UTC using pytz
Sparse sentiment scores	Limited emotional lexicon	Augmented with FinBERT
TA-Lib installation fails	Missing C dependencies	Used Conda: conda install -c conda-forge ta-lib
##Validation Metrics
✔ Sentiment Accuracy: 82% vs human-labeled test set
✔ Indicator Reliability: RSI signals matched 76% of price reversals
✔ Correlation Significance: p<0.05 for 3/5 tested stocks

# 5. Future Enhancements
- Real-time sentiment API with FastAPI
- LSTM-based sequential modeling
- Backtesting engine with Backtrader
