"""Document loader for development guidelines."""

from pathlib import Path
from typing import Optional


class DocumentLoader:
    """Loads and caches development documentation files."""
    
    def __init__(self):
        """Initialize document loader with empty cache."""
        self._cache: dict[str, str] = {}
    
    def load_document(self, file_path: str, use_cache: bool = True) -> str:
        """
        Load a documentation file.
        
        Args:
            file_path: Path to the documentation file
            use_cache: Whether to use cached version if available
        
        Returns:
            Content of the documentation file
        
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        if use_cache and file_path in self._cache:
            return self._cache[file_path]
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Documentation file not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._cache[file_path] = content
        return content
    
    def clear_cache(self, file_path: Optional[str] = None) -> None:
        """
        Clear the document cache.
        
        Args:
            file_path: Specific file to clear from cache, or None to clear all
        """
        if file_path is None:
            self._cache.clear()
        elif file_path in self._cache:
            del self._cache[file_path]
    
    def get_rules(self, rules_path: str) -> str:
        """Load coding rules documentation."""
        return self.load_document(rules_path)
    
    def get_skills(self, skills_path: str) -> str:
        """Load development skills documentation."""
        return self.load_document(skills_path)
    
    def get_steering(self, steering_path: str) -> str:
        """Load AI steering instructions."""
        return self.load_document(steering_path)
    
    def get_all_docs(self, rules_path: str, skills_path: str, steering_path: str) -> dict[str, str]:
        """
        Load all documentation files.
        
        Args:
            rules_path: Path to rules documentation
            skills_path: Path to skills documentation
            steering_path: Path to steering documentation
        
        Returns:
            Dictionary with all loaded documents
        """
        return {
            'rules': self.get_rules(rules_path),
            'skills': self.get_skills(skills_path),
            'steering': self.get_steering(steering_path)
        }
