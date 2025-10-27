"""Configuration management for MCP server."""

import yaml
from pathlib import Path
from typing import Any


class Config:
    """Configuration loader and accessor."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration from YAML file.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        self.config_path = Path(config_path)
        self._config: dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key using dot notation.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'server.name')
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        
        Example:
            >>> config.get('server.name')
            'AI Development Guidelines Server'
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    @property
    def server_name(self) -> str:
        """Get server name."""
        return self.get('server.name', 'MCP Server')
    
    @property
    def server_version(self) -> str:
        """Get server version."""
        return self.get('server.version', '1.0.0')
    
    @property
    def rules_path(self) -> str:
        """Get rules documentation path."""
        return self.get('documentation.rules_path', 'docs/rules.md')
    
    @property
    def skills_path(self) -> str:
        """Get skills documentation path."""
        return self.get('documentation.skills_path', 'docs/skills.md')
    
    @property
    def steering_path(self) -> str:
        """Get steering documentation path."""
        return self.get('documentation.steering_path', 'docs/steering.md')
    
    @property
    def ai_model(self) -> str:
        """Get AI model name."""
        return self.get('ai_orchestrator.model', 'claude-3-5-sonnet-20241022')
    
    @property
    def ai_max_tokens(self) -> int:
        """Get AI max tokens."""
        return self.get('ai_orchestrator.max_tokens', 4000)
    
    @property
    def ai_temperature(self) -> float:
        """Get AI temperature."""
        return self.get('ai_orchestrator.temperature', 0.7)
