import pandas as pd
from src.data_processing import DataProcessor
from src.text_analysis import TopicModeler
from src.time_series import TimeSeriesAnalyzer
from src.publisher_analysis import PublisherAnalyzer
import os

def main():
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Initialize components
    processor = DataProcessor()
    topic_modeler = TopicModeler()
    ts_analyzer = TimeSeriesAnalyzer()
    pub_analyzer = PublisherAnalyzer()
    
    # Load and process data
    print("Loading and processing data...")
    df = processor.process_raw_data('data/raw/fnspid.csv')
    
    # Topic Modeling
    print("Performing topic modeling...")
    dtm = topic_modeler.fit_model(df['cleaned_text'])
    topics = topic_modeler.get_topics()
    topic_modeler.visualize_topics(dtm, 'output/topic_visualization.html')
    
    # Time Series Analysis
    print("Analyzing time series patterns...")
    ts_analyzer.analyze_publication_frequency(df)
    ts_analyzer.analyze_intraday_patterns(df)
    
    # Publisher Analysis
    print("Analyzing publisher patterns...")
    pub_results = pub_analyzer.analyze_publishers(df)
    
    # Save results
    topics.to_csv('output/discovered_topics.csv')
    df.to_csv('output/processed_data.csv')
    print("Analysis complete. Results saved to output/ directory.")

if __name__ == "__main__":
    main()