"""Feedback collection system for MCP server."""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Any


class FeedbackCollector:
    """Collects and stores usage feedback and metrics."""
    
    def __init__(self, feedback_dir: str = "feedback"):
        """
        Initialize feedback collector.
        
        Args:
            feedback_dir: Directory to store feedback data
        """
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(exist_ok=True)
    
    def record_call(
        self,
        tool_name: str,
        arguments: dict,
        response_size: int,
        tokens_used: Optional[int] = None,
        response_time_ms: Optional[float] = None,
        success: bool = True,
        error: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> None:
        """
        Record an MCP tool call.
        
        Args:
            tool_name: Name of the tool called
            arguments: Arguments passed to the tool
            response_size: Size of response in characters
            tokens_used: Estimated tokens used
            response_time_ms: Response time in milliseconds
            success: Whether the call succeeded
            error: Error message if failed
            metadata: Additional metadata
        """
        timestamp = datetime.now()
        
        feedback_data = {
            "timestamp": timestamp.isoformat(),
            "tool_name": tool_name,
            "arguments": arguments,
            "response_size": response_size,
            "tokens_used": tokens_used,
            "response_time_ms": response_time_ms,
            "success": success,
            "error": error,
            "metadata": metadata or {}
        }
        
        filename = f"call_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.json"
        filepath = self.feedback_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(feedback_data, f, indent=2)
    
    def record_user_feedback(
        self,
        tool_name: str,
        rating: int,
        comment: Optional[str] = None,
        helpful: Optional[bool] = None,
        metadata: Optional[dict] = None
    ) -> None:
        """
        Record user feedback about a response.
        
        Args:
            tool_name: Name of the tool
            rating: Rating from 1-5
            comment: Optional text comment
            helpful: Whether response was helpful
            metadata: Additional metadata
        """
        timestamp = datetime.now()
        
        feedback_data = {
            "timestamp": timestamp.isoformat(),
            "type": "user_feedback",
            "tool_name": tool_name,
            "rating": rating,
            "comment": comment,
            "helpful": helpful,
            "metadata": metadata or {}
        }
        
        filename = f"feedback_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.json"
        filepath = self.feedback_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(feedback_data, f, indent=2)
    
    def get_summary(self, days: int = 7) -> dict:
        """
        Get summary of recent feedback.
        
        Args:
            days: Number of days to include
        
        Returns:
            Summary statistics
        """
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        
        total_calls = 0
        successful_calls = 0
        total_tokens = 0
        tool_counts = {}
        
        for file in self.feedback_dir.glob("call_*.json"):
            with open(file, 'r') as f:
                data = json.load(f)
                
                call_time = datetime.fromisoformat(data["timestamp"])
                if call_time < cutoff:
                    continue
                
                total_calls += 1
                if data.get("success"):
                    successful_calls += 1
                
                if data.get("tokens_used"):
                    total_tokens += data["tokens_used"]
                
                tool = data.get("tool_name", "unknown")
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        return {
            "period_days": days,
            "total_calls": total_calls,
            "successful_calls": successful_calls,
            "success_rate": successful_calls / total_calls if total_calls > 0 else 0,
            "total_tokens_used": total_tokens,
            "avg_tokens_per_call": total_tokens / total_calls if total_calls > 0 else 0,
            "tool_usage": tool_counts
        }
