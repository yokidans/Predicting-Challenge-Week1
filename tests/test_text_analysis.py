import pytest
from src.text_analysis import TopicModeler

def test_topic_modeling():
    texts = [
        "apple stock hits new high",
        "fed raises interest rates",
        "tech stocks rally continues"
    ]
    
    modeler = TopicModeler(n_topics=2)
    dtm = modeler.fit_model(texts)
    topics = modeler.get_topics()
    
    assert len(topics) == 2
    assert len(topics.iloc[0]['top_words']) == 10