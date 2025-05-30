import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download(['stopwords', 'wordnet'])

class DataProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english')) | {'said', 'company', 'inc'}
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        text = re.sub(r'[^a-zA-Z\s]', '', str(text), re.I|re.A)
        tokens = text.lower().split()
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens 
                 if t not in self.stop_words and len(t) > 2]
        return ' '.join(tokens)

    def process_raw_data(self, filepath):
        df = pd.read_csv(filepath, parse_dates=['date'])
        df.set_index('date', inplace=True)
        df['headline_length'] = df['headline'].apply(len)
        df['cleaned_text'] = df['headline'].apply(self.clean_text)
        return df