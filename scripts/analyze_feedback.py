#!/usr/bin/env python3
"""Analyze user feedback and usage patterns."""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict


def analyze_feedback():
    """Analyze collected feedback data."""
    print("Analyzing feedback and usage patterns...")
    
    feedback_dir = Path("feedback")
    if not feedback_dir.exists():
        print("No feedback data found. Creating sample analytics...")
        feedback_dir.mkdir(exist_ok=True)
        
        sample_data = {
            "message": "No feedback data collected yet",
            "recommendations": [
                "Start collecting MCP call metrics",
                "Track tool usage patterns",
                "Monitor token consumption",
                "Collect user ratings and comments"
            ]
        }
        
        analytics_dir = Path("analytics")
        analytics_dir.mkdir(exist_ok=True)
        
        with open(analytics_dir / "feedback_analysis.json", 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print("✓ Sample analytics created")
        return
    
    feedback_files = list(feedback_dir.glob("*.json"))
    
    if not feedback_files:
        print("No feedback files found")
        return
    
    tool_usage = Counter()
    token_usage = defaultdict(list)
    response_times = defaultdict(list)
    
    for file in feedback_files:
        with open(file, 'r') as f:
            data = json.load(f)
            
            if "tool_name" in data:
                tool_usage[data["tool_name"]] += 1
            
            if "tokens_used" in data:
                tool = data.get("tool_name", "unknown")
                token_usage[tool].append(data["tokens_used"])
            
            if "response_time_ms" in data:
                tool = data.get("tool_name", "unknown")
                response_times[tool].append(data["response_time_ms"])
    
    analytics = {
        "analysis_time": datetime.now().isoformat(),
        "total_calls": sum(tool_usage.values()),
        "tool_usage": dict(tool_usage),
        "token_stats": {
            tool: {
                "total": sum(tokens),
                "avg": sum(tokens) / len(tokens) if tokens else 0,
                "max": max(tokens) if tokens else 0,
                "min": min(tokens) if tokens else 0
            }
            for tool, tokens in token_usage.items()
        },
        "response_time_stats": {
            tool: {
                "avg_ms": sum(times) / len(times) if times else 0,
                "max_ms": max(times) if times else 0,
                "min_ms": min(times) if times else 0
            }
            for tool, times in response_times.items()
        }
    }
    
    analytics_dir = Path("analytics")
    analytics_dir.mkdir(exist_ok=True)
    
    output_file = analytics_dir / f"feedback_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(analytics, f, indent=2)
    
    print(f"✓ Analytics saved to {output_file}")
    print(f"  Total calls analyzed: {analytics['total_calls']}")
    print(f"  Most used tool: {tool_usage.most_common(1)[0] if tool_usage else 'N/A'}")


if __name__ == "__main__":
    analyze_feedback()
