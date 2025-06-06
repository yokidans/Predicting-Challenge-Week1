import pytest
from src.data.loader import DataLoader
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

def test_data_loader():
    loader = DataLoader()
    assert loader is not None
class TestDataLoading:
    def test_csv_loading(self):
        loader = DataLoader()
        data = loader.load_from_csv('TEST')
        assert not data.empty