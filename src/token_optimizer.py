"""Token optimizer for efficient MCP responses."""

from typing import Optional
import re


class TokenOptimizer:
    """Optimizes content to reduce token usage while maintaining quality."""
    
    def __init__(self, max_tokens: Optional[int] = None):
        """
        Initialize token optimizer.
        
        Args:
            max_tokens: Maximum tokens allowed in response (None for no limit)
        """
        self.max_tokens = max_tokens
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count using 4-character approximation.
        
        Args:
            text: Text to estimate
        
        Returns:
            Estimated token count
        """
        return len(text) // 4
    
    def optimize_content(self, content: str, target_tokens: Optional[int] = None) -> str:
        """
        Optimize content to fit within token budget.
        
        Args:
            content: Content to optimize
            target_tokens: Target token count (uses self.max_tokens if None)
        
        Returns:
            Optimized content
        """
        target = target_tokens or self.max_tokens
        
        if target is None:
            return content
        
        current_tokens = self.estimate_tokens(content)
        
        if current_tokens <= target:
            return content
        
        reduction_ratio = target / current_tokens
        
        optimized = self._smart_truncate(content, reduction_ratio)
        
        return optimized
    
    def _smart_truncate(self, content: str, ratio: float) -> str:
        """
        Intelligently truncate content while preserving structure.
        
        Args:
            content: Content to truncate
            ratio: Target size ratio (0.0 to 1.0)
        
        Returns:
            Truncated content
        """
        lines = content.split('\n')
        
        target_lines = int(len(lines) * ratio)
        
        headers = []
        important_lines = []
        other_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if stripped.startswith('#'):
                headers.append((i, line))
            elif stripped.startswith('-') or stripped.startswith('*') or stripped.startswith('1.'):
                important_lines.append((i, line))
            elif stripped and not stripped.startswith('```'):
                other_lines.append((i, line))
        
        selected_indices = set()
        
        for i, line in headers:
            selected_indices.add(i)
        
        important_count = min(len(important_lines), target_lines - len(headers))
        for i, line in important_lines[:important_count]:
            selected_indices.add(i)
        
        remaining = target_lines - len(selected_indices)
        for i, line in other_lines[:remaining]:
            selected_indices.add(i)
        
        result_lines = []
        for i, line in enumerate(lines):
            if i in selected_indices:
                result_lines.append(line)
        
        result = '\n'.join(result_lines)
        
        if len(result) < len(content) * 0.5:
            result += "\n\n... (content truncated for token optimization)"
        
        return result
    
    def get_summary(self, content: str, max_length: int = 500) -> str:
        """
        Get a summary of content.
        
        Args:
            content: Content to summarize
            max_length: Maximum character length
        
        Returns:
            Summary text
        """
        lines = content.split('\n')
        
        headers = [line.strip() for line in lines if line.strip().startswith('#')]
        
        if headers:
            summary = "Table of Contents:\n" + '\n'.join(headers[:10])
        else:
            summary = content[:max_length]
        
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        
        return summary
    
    def get_stats(self, content: str) -> dict:
        """
        Get statistics about content token usage.
        
        Args:
            content: Content to analyze
        
        Returns:
            Dictionary with statistics
        """
        return {
            "characters": len(content),
            "estimated_tokens": self.estimate_tokens(content),
            "lines": len(content.split('\n')),
            "words": len(content.split()),
            "code_blocks": content.count('```') // 2,
            "headers": len([l for l in content.split('\n') if l.strip().startswith('#')])
        }
