from urllib.parse import urlparse
from textblob import TextBlob
import networkx as nx

class PublisherAnalyzer:
    def extract_domain(self, publisher):
        if '@' in str(publisher):
            return publisher.split('@')[-1]
        elif 'http' in str(publisher):
            return urlparse(publisher).netloc
        return publisher

    def analyze_publishers(self, df):
        # Market share analysis
        publisher_counts = df['publisher'].value_counts(normalize=True) * 100
        top_publishers = publisher_counts.head(10)
        
        # Sentiment analysis
        df['sentiment'] = df['headline'].apply(lambda x: TextBlob(x).sentiment.polarity)
        publisher_sentiment = df.groupby('publisher')['sentiment'].mean().sort_values()
        
        # Domain analysis
        df['publisher_domain'] = df['publisher'].apply(self.extract_domain)
        
        return {
            'market_share': publisher_counts,
            'sentiment': publisher_sentiment,
            'domains': df['publisher_domain'].value_counts()
        }