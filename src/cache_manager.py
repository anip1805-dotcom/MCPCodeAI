"""Cache manager for compressed documentation delivery."""

import gzip
import json
import pickle
from pathlib import Path
from typing import Optional, Literal


CacheFormat = Literal["json", "json_gz", "pickle", "pickle_gz"]


class CacheManager:
    """Manages compressed cache for efficient documentation delivery."""
    
    def __init__(self, cache_dir: str = "cache"):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory containing cache files
        """
        self.cache_dir = Path(cache_dir)
        self._manifest: Optional[dict] = None
    
    def load_manifest(self) -> dict:
        """Load cache manifest."""
        if self._manifest is not None:
            return self._manifest
        
        manifest_path = self.cache_dir / "manifest.json"
        
        if not manifest_path.exists():
            return {}
        
        with open(manifest_path, 'r') as f:
            self._manifest = json.load(f)
        
        return self._manifest
    
    def get_cache(self, format: CacheFormat = "json_gz") -> Optional[dict]:
        """
        Load cache in specified format.
        
        Args:
            format: Cache format to load
        
        Returns:
            Cache data or None if not available
        """
        manifest = self.load_manifest()
        
        if not manifest or "files" not in manifest:
            return None
        
        filename = manifest["files"].get(format)
        if not filename:
            return None
        
        filepath = self.cache_dir / filename
        if not filepath.exists():
            return None
        
        if format == "json":
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        elif format == "json_gz":
            with gzip.open(filepath, 'rb') as f:
                return json.loads(f.read().decode('utf-8'))
        
        elif format == "pickle":
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        
        elif format == "pickle_gz":
            with gzip.open(filepath, 'rb') as f:
                return pickle.load(f)
        
        return None
    
    def get_document(self, doc_name: str, format: CacheFormat = "json_gz") -> Optional[str]:
        """
        Get a specific document from cache.
        
        Args:
            doc_name: Document name (rules, skills, or steering)
            format: Cache format to use
        
        Returns:
            Document content or None
        """
        cache_data = self.get_cache(format)
        
        if not cache_data or "documents" not in cache_data:
            return None
        
        return cache_data["documents"].get(doc_name)
    
    def get_cache_info(self) -> dict:
        """
        Get information about available caches.
        
        Returns:
            Cache information
        """
        manifest = self.load_manifest()
        
        if not manifest:
            return {
                "available": False,
                "message": "No cache available"
            }
        
        return {
            "available": True,
            "version": manifest.get("version"),
            "build_time": manifest.get("build_time"),
            "formats": list(manifest.get("files", {}).keys()),
            "sizes": manifest.get("sizes", {}),
            "recommended_format": "json_gz"
        }
    
    def get_optimal_format(self) -> CacheFormat:
        """
        Get the most efficient cache format available.
        
        Returns:
            Optimal cache format
        """
        manifest = self.load_manifest()
        
        if not manifest or "sizes" not in manifest:
            return "json"
        
        sizes = manifest["sizes"]
        
        if "pickle_gz" in sizes and "json_gz" in sizes:
            return "pickle_gz" if sizes["pickle_gz"] < sizes["json_gz"] else "json_gz"
        elif "json_gz" in sizes:
            return "json_gz"
        elif "pickle" in sizes:
            return "pickle"
        else:
            return "json"
