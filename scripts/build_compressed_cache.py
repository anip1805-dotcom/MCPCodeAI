#!/usr/bin/env python3
"""Build compressed cache files for efficient MCP delivery."""

import gzip
import json
import pickle
from pathlib import Path
from datetime import datetime
from src.utils.config import Config
from src.utils.document_loader import DocumentLoader


def build_compressed_cache():
    """Build compressed cache of all documentation."""
    print("Building compressed documentation cache...")
    
    config = Config()
    doc_loader = DocumentLoader()
    
    all_docs = doc_loader.get_all_docs(
        config.rules_path,
        config.skills_path,
        config.steering_path
    )
    
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    
    cache_data = {
        "version": config.server_version,
        "build_time": datetime.now().isoformat(),
        "documents": all_docs,
        "metadata": {
            "rules_size": len(all_docs['rules']),
            "skills_size": len(all_docs['skills']),
            "steering_size": len(all_docs['steering']),
            "total_size": sum(len(doc) for doc in all_docs.values())
        }
    }
    
    json_path = cache_dir / "docs_cache.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2)
    json_size = json_path.stat().st_size
    print(f"  - JSON cache: {json_size:,} bytes")
    
    gzip_path = cache_dir / "docs_cache.json.gz"
    with gzip.open(gzip_path, 'wb') as f:
        f.write(json.dumps(cache_data).encode('utf-8'))
    gzip_size = gzip_path.stat().st_size
    compression_ratio = (1 - gzip_size / json_size) * 100
    print(f"  - Gzipped cache: {gzip_size:,} bytes ({compression_ratio:.1f}% compression)")
    
    pickle_path = cache_dir / "docs_cache.pkl"
    with open(pickle_path, 'wb') as f:
        pickle.dump(cache_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    pickle_size = pickle_path.stat().st_size
    print(f"  - Pickle cache: {pickle_size:,} bytes")
    
    pickle_gzip_path = cache_dir / "docs_cache.pkl.gz"
    with gzip.open(pickle_gzip_path, 'wb') as f:
        pickle.dump(cache_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    pickle_gzip_size = pickle_gzip_path.stat().st_size
    pickle_compression_ratio = (1 - pickle_gzip_size / pickle_size) * 100
    print(f"  - Gzipped pickle cache: {pickle_gzip_size:,} bytes ({pickle_compression_ratio:.1f}% compression)")
    
    print(f"\n✓ Cache built successfully!")
    print(f"  Total uncompressed size: {cache_data['metadata']['total_size']:,} bytes")
    print(f"  Best compressed size: {min(gzip_size, pickle_gzip_size):,} bytes")
    print(f"  Overall compression: {(1 - min(gzip_size, pickle_gzip_size) / cache_data['metadata']['total_size']) * 100:.1f}%")
    
    cache_manifest = {
        "files": {
            "json": str(json_path.name),
            "json_gz": str(gzip_path.name),
            "pickle": str(pickle_path.name),
            "pickle_gz": str(pickle_gzip_path.name)
        },
        "sizes": {
            "json": json_size,
            "json_gz": gzip_size,
            "pickle": pickle_size,
            "pickle_gz": pickle_gzip_size
        },
        "build_time": cache_data["build_time"],
        "version": cache_data["version"]
    }
    
    with open(cache_dir / "manifest.json", 'w') as f:
        json.dump(cache_manifest, f, indent=2)
    
    return cache_data


if __name__ == "__main__":
    build_compressed_cache()
