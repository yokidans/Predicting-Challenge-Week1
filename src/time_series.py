from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt

class TimeSeriesAnalyzer:
    def analyze_publication_frequency(self, df):
        daily_counts = df['headline'].resample('D').count()
        
        # STL Decomposition
        decomp = STL(daily_counts.fillna(0), period=7).fit()
        decomp.plot()
        plt.savefig('output/stl_decomposition.png')
        plt.close()
        
        return decomp

    def analyze_intraday_patterns(self, df):
        df['hour'] = df.index.hour
        hourly_counts = df.groupby('hour').size()
        
        plt.figure(figsize=(12,6))
        hourly_counts.plot(kind='bar', color='steelblue')
        plt.title('Article Publication by Hour')
        plt.xlabel('Hour of Day (UTC)')
        plt.ylabel('Number of Articles')
        plt.savefig('output/hourly_distribution.png')
        plt.close()
        
        return hourly_counts