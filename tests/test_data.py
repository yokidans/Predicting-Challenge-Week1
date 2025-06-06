import pytest
from src.data.loader import DataLoader

class TestDataLoading:
    def test_csv_loading(self):
        loader = DataLoader()
        data = loader.load_from_csv('TEST')
        assert not data.empty