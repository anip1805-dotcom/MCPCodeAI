"""Tests for token optimizer."""

import pytest
from src.token_optimizer import TokenOptimizer


def test_token_estimation():
    """Test token estimation."""
    optimizer = TokenOptimizer()
    
    text = "a" * 400
    tokens = optimizer.estimate_tokens(text)
    assert tokens == 100
    
    text = "Hello world, this is a test"
    tokens = optimizer.estimate_tokens(text)
    assert tokens > 0


def test_optimize_content():
    """Test content optimization."""
    optimizer = TokenOptimizer(max_tokens=100)
    
    long_text = "Hello world. " * 200
    optimized = optimizer.optimize_content(long_text, target_tokens=50)
    
    assert len(optimized) < len(long_text)
    assert optimizer.estimate_tokens(optimized) <= 50


def test_get_stats():
    """Test statistics generation."""
    optimizer = TokenOptimizer()
    
    text = """# Header
    
Some content here.

```python
def hello():
    print("world")
```
"""
    
    stats = optimizer.get_stats(text)
    
    assert stats["characters"] > 0
    assert stats["estimated_tokens"] > 0
    assert stats["lines"] > 0
    assert stats["code_blocks"] == 1
    assert stats["headers"] == 1


if __name__ == "__main__":
    pytest.main([__file__])
