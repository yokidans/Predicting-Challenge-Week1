import pytest
from src.data_processing import DataProcessor

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'headline': ['Apple stock hits record high!', 'Fed raises interest rates'],
        'date': ['2025-01-01', '2025-01-02']
    })

def test_data_processing(sample_data):
    processor = DataProcessor()
    processed = processor.process_raw_data(sample_data)
    
    assert 'cleaned_text' in processed.columns
    assert processed['headline_length'].iloc[0] == 24
    assert 'apple' in processed['cleaned_text'].iloc[0]