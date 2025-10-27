"""Tests for feedback collector."""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from src.feedback_collector import FeedbackCollector


@pytest.fixture
def temp_feedback_dir():
    """Create a temporary feedback directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_record_call(temp_feedback_dir):
    """Test recording a tool call."""
    collector = FeedbackCollector(temp_feedback_dir)
    
    collector.record_call(
        tool_name="get_coding_rules",
        arguments={},
        response_size=5000,
        tokens_used=1250,
        response_time_ms=150.5,
        success=True
    )
    
    feedback_files = list(Path(temp_feedback_dir).glob("call_*.json"))
    assert len(feedback_files) == 1
    
    with open(feedback_files[0], 'r') as f:
        data = json.load(f)
    
    assert data["tool_name"] == "get_coding_rules"
    assert data["tokens_used"] == 1250
    assert data["success"] is True


def test_record_user_feedback(temp_feedback_dir):
    """Test recording user feedback."""
    collector = FeedbackCollector(temp_feedback_dir)
    
    collector.record_user_feedback(
        tool_name="get_coding_rules",
        rating=5,
        comment="Very helpful!",
        helpful=True
    )
    
    feedback_files = list(Path(temp_feedback_dir).glob("feedback_*.json"))
    assert len(feedback_files) == 1
    
    with open(feedback_files[0], 'r') as f:
        data = json.load(f)
    
    assert data["tool_name"] == "get_coding_rules"
    assert data["rating"] == 5
    assert data["helpful"] is True


def test_get_summary(temp_feedback_dir):
    """Test getting feedback summary."""
    collector = FeedbackCollector(temp_feedback_dir)
    
    for i in range(5):
        collector.record_call(
            tool_name="get_coding_rules",
            arguments={},
            response_size=5000,
            tokens_used=1250,
            response_time_ms=150,
            success=True
        )
    
    summary = collector.get_summary(days=7)
    
    assert summary["total_calls"] == 5
    assert summary["successful_calls"] == 5
    assert summary["success_rate"] == 1.0
    assert summary["total_tokens_used"] == 6250


if __name__ == "__main__":
    pytest.main([__file__])
