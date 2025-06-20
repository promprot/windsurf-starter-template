"""Configuration management for the Windsurf agent.

This module provides Pydantic models for managing the agent's configuration,
with support for loading from JSON files and environment variables.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field, HttpUrl, validator, BaseSettings, root_validator

# Type variable for generic model parsing
T = TypeVar('T', bound='BaseModel')

def parse_env_var(name: str, default: Any = None) -> Any:
    """Parse environment variable with support for JSON deserialization."""
    value = os.getenv(name, None)
    if value is None:
        return default
    
    # Try to parse as JSON, fallback to string
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


class MemoryConfig(BaseModel):
    """Configuration for the agent's memory settings."""
    enabled: bool = True
    persistence: bool = True
    max_entries: int = Field(1000, ge=1, le=100000)


class ToolsConfig(BaseModel):
    """Configuration for the agent's tools."""
    auto_discover: bool = True
    directory: str = "src/tools"
    timeout_seconds: int = Field(30, ge=1, le=300)


class LoggingConfig(BaseModel):
    """Configuration for logging."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "logs/agent.log"
    max_size_mb: int = Field(10, ge=1, le=100)
    backup_count: int = Field(5, ge=0, le=100)


class RateLimitConfig(BaseModel):
    """Configuration for rate limiting."""
    enabled: bool = True
    max_requests: int = Field(100, ge=1, le=10000)
    window_seconds: int = Field(60, ge=1, le=3600)


class CorsConfig(BaseModel):
    """Configuration for CORS."""
    enabled: bool = True
    allow_credentials: bool = True
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE"]
    allowed_headers: List[str] = ["*"]
    exposed_headers: List[str] = []
    max_age: int = Field(600, ge=0, le=86400)


class SecurityConfig(BaseModel):
    """Security-related configuration."""
    require_authentication: bool = False
    api_key: str = ""
    allowed_origins: List[Union[HttpUrl, str]] = ["*"]
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    cors: CorsConfig = Field(default_factory=CorsConfig)


class HealthCheckConfig(BaseModel):
    """Health check endpoint configuration."""
    enabled: bool = True
    endpoint: str = "/health"
    live_endpoint: str = "/health/live"
    ready_endpoint: str = "/health/ready"


class MonitoringConfig(BaseModel):
    """Monitoring and metrics configuration."""
    enabled: bool = True
    port: int = Field(9090, ge=1024, le=65535)
    endpoint: str = "/metrics"
    health_check: HealthCheckConfig = Field(default_factory=HealthCheckConfig)


class VersionControlConfig(BaseModel):
    """Version control configuration."""
    auto_commit: bool = False
    branch: str = "main"
    remote: str = "origin"
    commit_message: str = "chore: auto-update config"


class AgentConfig(BaseModel):
    """Main configuration model for the Windsurf agent."""
    name: str = "windsurf-agent"
    version: str = "0.1.0"
    description: str = "A Windsurf agent template"
    entry_point: str = "src/main.py"
    
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    tools: ToolsConfig = Field(default_factory=ToolsConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    version_control: VersionControlConfig = Field(default_factory=VersionControlConfig)

    @classmethod
    def from_json_file(cls: Type[T], file_path: Union[str, Path]) -> T:
        """Load configuration from a JSON file.
        
        Args:
            file_path: Path to the JSON configuration file.
            
        Returns:
            AgentConfig: Loaded configuration.
            
        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            ValidationError: If the configuration is invalid.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
            
        with open(path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            
        return cls.parse_obj(config_data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary.
        
        Returns:
            Dict: Dictionary representation of the configuration.
        """
        return self.dict(by_alias=True, exclude_unset=True)
    
    def update_from_env(self) -> None:
        """Update configuration from environment variables.
        
        This method updates the configuration with values from environment variables.
        Environment variables should be prefixed with 'WINDSURF_' and use double underscore
        to denote nested fields (e.g., WINDSURF_LOGGING_LEVEL).
        """
        prefix = 'WINDSURF_'
        
        for field_name, field in self.__fields__.items():
            env_name = f"{prefix}{field_name.upper()}"
            
            # Handle nested models
            if hasattr(field.type_, '__base__') and issubclass(field.type_, BaseModel):
                nested_config = getattr(self, field_name)
                if nested_config is not None:
                    nested_config.update_from_env()
                continue
                
            # Handle list of models
            if (hasattr(field.type_, '__origin__') and 
                field.type_.__origin__ is list and 
                hasattr(field.type_.__args__[0], '__base__') and 
                issubclass(field.type_.__args__[0], BaseModel)):
                
                list_configs = getattr(self, field_name, [])
                for item in list_configs:
                    item.update_from_env()
                continue
                
            # Handle simple fields
            env_value = os.getenv(env_name)
            if env_value is not None:
                try:
                    # Try to parse the value as JSON first
                    parsed_value = json.loads(env_value)
                    setattr(self, field_name, parsed_value)
                except (json.JSONDecodeError, TypeError):
                    # Fall back to string if not valid JSON
                    setattr(self, field_name, env_value)
    
    @classmethod
    def from_env(cls: Type[T], prefix: str = 'WINDSURF_') -> T:
        """Create a config instance from environment variables.
        
        Args:
            prefix: Prefix for environment variables
            
        Returns:
            AgentConfig: New config instance with values from environment variables
        """
        # First create a default config
        config = cls()
        # Then update it with environment variables
        config.update_from_env()
        return config
        
    def to_env_file(self, file_path: Union[str, Path], prefix: str = 'WINDSURF_') -> None:
        """Export the configuration to an environment file.
        
        Args:
            file_path: Path to the output file
            prefix: Prefix for environment variables
        """
        env_lines = [f"# Auto-generated environment variables for {self.__class__.__name__}\n"]
        
        def process_value(value: Any) -> str:
            """Convert a value to a string suitable for an env file."""
            if isinstance(value, (dict, list)):
                return json.dumps(value)
            return str(value)
        
        def add_to_env(data: Dict[str, Any], current_prefix: str = '') -> None:
            """Recursively add config items to environment variables."""
            for key, value in data.items():
                env_name = f"{current_prefix}{key.upper()}"
                if isinstance(value, dict):
                    add_to_env(value, f"{env_name}_")
                elif isinstance(value, list) and value and isinstance(value[0], dict):
                    for i, item in enumerate(value):
                        add_to_env(item, f"{env_name}_{i}_")
                else:
                    env_lines.append(f"{prefix}{env_name}={process_value(value)}\n")
        
        add_to_env(self.dict(exclude_unset=True))
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(env_lines)


def load_config(file_path: Union[str, Path, None] = None, 
               use_env: bool = True) -> AgentConfig:
    """Load the agent configuration from a file and/or environment variables.
    
    Args:
        file_path: Path to the configuration file. If None, uses default location.
        use_env: Whether to apply environment variable overrides.
        
    Returns:
        AgentConfig: The loaded configuration.
        
    Raises:
        FileNotFoundError: If the configuration file doesn't exist and file_path was provided.
        ValidationError: If the configuration is invalid.
    """
    # If no file path provided, try to load from default location
    if file_path is None:
        default_path = Path(".windsurf/agent_settings.json")
        if default_path.exists():
            config = AgentConfig.from_json_file(default_path)
        else:
            # If default file doesn't exist, create a default config
            config = AgentConfig()
    else:
        config = AgentConfig.from_json_file(file_path)
    
    # Apply environment variable overrides if enabled
    if use_env:
        config.update_from_env()
    
    return config
