from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn

class TopicModeler:
    def __init__(self, n_topics=5):
        self.n_topics = n_topics
        self.vectorizer = CountVectorizer(
            max_df=0.95,
            min_df=2,
            ngram_range=(1,2),
            stop_words='english'
        )
        self.lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42
        )

    def fit_model(self, texts):
        dtm = self.vectorizer.fit_transform(texts)
        self.lda.fit(dtm)
        return dtm

    def visualize_topics(self, dtm, output_path):
        vis = pyLDAvis.sklearn.prepare(self.lda, dtm, self.vectorizer)
        pyLDAvis.save_html(vis, output_path)

    def get_topics(self, n_words=10):
        feature_names = self.vectorizer.get_feature_names_out()
        topics = []
        for topic_idx, topic in enumerate(self.lda.components_):
            topics.append({
                'topic_id': topic_idx,
                'top_words': [feature_names[i] for i in topic.argsort()[:-n_words-1:-1]]
            })
        return pd.DataFrame(topics)