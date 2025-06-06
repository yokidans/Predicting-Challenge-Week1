# Financial News Sentiment Analysis

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-1.3%2B-orange)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0%2B-yellowgreen)
![NLTK](https://img.shields.io/badge/NLTK-3.6%2B-lightgrey)

A comprehensive pipeline for analyzing financial news sentiment, extracting key topics, and visualizing temporal patterns in news publications.

## Features

- **Text Preprocessing**: Advanced cleaning with lemmatization and custom stopwords
- **Topic Modeling**: LDA implementation with optimized parameters
- **Sentiment Analysis**: Polarity and subjectivity scoring using TextBlob
- **Time Series Analysis**: STL decomposition and publication frequency patterns
- **Publisher Analytics**: Market share and sentiment by news source
- **Interactive Visualizations**: Topic word clouds, temporal trends, and sentiment distributions

## Requirements

    `bash
          pip install pandas numpy matplotlib seaborn textblob nltk scikit-learn statsmodels wordcloud tqdm

   
## Features
Data Preparation
- Place your financial news dataset as fnspid_dataset.csv in the project root

- Required columns: date, headline, publisher

- Date format should be parseable by pandas (ISO8601 preferred)

## Analysis Pipeline
1. Descriptive Statistics
 - Character and word count distributions

 - Basic dataset metrics

2. Topic Modeling
- Custom text cleaning pipeline

- CountVectorizer with optimal parameters

- Latent Dirichlet Allocation (LDA) implementation

- Interactive topic visualization


# Example topic output
    Topic 1: stock market shares trading company investors price...
    Topic 2: bank federal reserve interest rates economy...
    https://sample_images/topics.png

3. Time Series Analysis
- Daily/Weekly/Monthly publication frequencies

- STL decomposition (trend, seasonality, residuals)

- Intraday publication patterns

python
# Example time series output
     Daily Counts:
     2023-01-01    142
     2023-01-02    156
     2023-01-03    201
     https://sample_images/stl_decomposition.png

4. Publisher Analytics
- Market share by publication volume

- Domain extraction and normalization

- Sentiment analysis by publisher

      https://sample_images/publisher_share.png

5. Sentiment Analysis
- Polarity (-1 to 1) and subjectivity (0 to 1) scoring

- Temporal sentiment trends

- Publisher sentiment comparison

python
# Example sentiment output
               polarity  subjectivity
    publisher                        
    Reuters         0.12        0.45
    Bloomberg       0.08        0.42
    Financial Times 0.15        0.51
     Output Files
    File	Description
    processed_financial_news.csv	Cleaned dataset with sentiment scores
    discovered_topics.csv	Extracted topics and key words
    publisher_stats.csv	Aggregated publisher metrics
    *.png	All generated visualizations
Customization
Modify these parameters in the notebook:

     python
    # Topic modeling
    N_TOPICS = 5           # Number of topics to extract
    MAX_FEATURES = 5000    # Maximum vocabulary size

    # Time series
    RESAMPLE_FREQ = 'D'    # 'D'aily, 'W'weekly, 'M'onthly

    # Visualization
    COLOR_PALETTE = 'viridis'  # matplotlib colormap
## Troubleshooting
### Common Issues:
- Date parsing errors:

- Check your CSV date format

- Explicitly specify format: pd.to_datetime(..., format='%Y-%m-%d')

### Memory errors:

- Reduce sample size: working_df = df.sample(5000)

- Decrease MAX_FEATURES

### Visualization issues:

- Update libraries: pip install --upgrade seaborn matplotlib

- Restart kernel after installation

# License
MIT License - Free for academic and commercial use
