"""Tests for cache manager."""

import pytest
import tempfile
import shutil
from pathlib import Path
from src.cache_manager import CacheManager


@pytest.fixture
def temp_cache_dir():
    """Create a temporary cache directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_cache_manager_no_cache(temp_cache_dir):
    """Test cache manager when no cache exists (fallback behavior)."""
    cache_manager = CacheManager(temp_cache_dir)
    
    cache_info = cache_manager.get_cache_info()
    assert cache_info["available"] is False
    assert "No cache available" in cache_info["message"]
    
    cache_data = cache_manager.get_cache()
    assert cache_data is None
    
    doc = cache_manager.get_document("rules")
    assert doc is None


def test_cache_manager_with_cache():
    """Test cache manager with actual cache."""
    cache_manager = CacheManager("cache")
    
    cache_info = cache_manager.get_cache_info()
    if cache_info.get("available"):
        assert "version" in cache_info
        assert "formats" in cache_info
        assert "json_gz" in cache_info.get("formats", [])
        
        cache_data = cache_manager.get_cache("json_gz")
        assert cache_data is not None
        assert "documents" in cache_data
        
        rules = cache_manager.get_document("rules", "json_gz")
        assert rules is not None
        assert len(rules) > 0


def test_optimal_format():
    """Test optimal format selection."""
    cache_manager = CacheManager("cache")
    
    optimal = cache_manager.get_optimal_format()
    assert optimal in ["json", "json_gz", "pickle", "pickle_gz"]


if __name__ == "__main__":
    pytest.main([__file__])
