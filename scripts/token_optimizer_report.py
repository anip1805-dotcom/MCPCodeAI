#!/usr/bin/env python3
"""Generate token optimization report."""

import json
from pathlib import Path
from datetime import datetime
from src.utils.config import Config
from src.utils.document_loader import DocumentLoader


def count_tokens_estimate(text: str) -> int:
    """Estimate token count (rough approximation: 1 token ≈ 4 characters)."""
    return len(text) // 4


def generate_token_report():
    """Generate token usage optimization report."""
    print("Generating token optimization report...")
    
    config = Config()
    doc_loader = DocumentLoader()
    
    all_docs = doc_loader.get_all_docs(
        config.rules_path,
        config.skills_path,
        config.steering_path
    )
    
    report = {
        "report_time": datetime.now().isoformat(),
        "version": config.server_version,
        "documents": {}
    }
    
    for doc_name, doc_content in all_docs.items():
        char_count = len(doc_content)
        estimated_tokens = count_tokens_estimate(doc_content)
        
        lines = doc_content.split('\n')
        
        report["documents"][doc_name] = {
            "characters": char_count,
            "estimated_tokens": estimated_tokens,
            "lines": len(lines),
            "avg_tokens_per_line": estimated_tokens / len(lines) if lines else 0,
            "optimization_suggestions": []
        }
        
        if estimated_tokens > 3000:
            report["documents"][doc_name]["optimization_suggestions"].append(
                "Consider splitting into multiple smaller documents"
            )
        
        if char_count / len(lines) > 200:
            report["documents"][doc_name]["optimization_suggestions"].append(
                "Lines are long - consider breaking into paragraphs"
            )
        
        code_blocks = doc_content.count('```')
        if code_blocks > 10:
            report["documents"][doc_name]["optimization_suggestions"].append(
                f"Many code examples ({code_blocks // 2}) - consider external references"
            )
    
    total_tokens = sum(d["estimated_tokens"] for d in report["documents"].values())
    report["summary"] = {
        "total_estimated_tokens": total_tokens,
        "total_characters": sum(d["characters"] for d in report["documents"].values()),
        "compression_potential": "Use gzip compression for ~60-70% reduction",
        "caching_recommendation": "Enable client-side caching for frequently requested docs"
    }
    
    report["optimization_recommendations"] = [
        "Use compressed cache files (JSON.gz or pickle.gz) for delivery",
        "Implement chunking for large documents",
        "Cache frequently accessed documentation client-side",
        "Consider summarization for overview requests",
        "Use resource URIs for selective loading"
    ]
    
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    output_file = reports_dir / f"token_usage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Token report saved to {output_file}")
    print(f"  Total estimated tokens: {total_tokens:,}")
    print(f"  Optimization potential: High (compression + caching)")
    
    for doc_name, doc_data in report["documents"].items():
        print(f"\n  {doc_name}:")
        print(f"    - {doc_data['estimated_tokens']:,} tokens")
        if doc_data['optimization_suggestions']:
            print(f"    - Suggestions: {len(doc_data['optimization_suggestions'])}")


if __name__ == "__main__":
    generate_token_report()
