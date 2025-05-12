#!/usr/bin/env python3
"""
Server Deployment Configuration for AI-PsychDoodle-Analyzer
"""

import os
import logging
import yaml
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ServerConfig:
    """
    Server deployment configuration for AI-PsychDoodle-Analyzer
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize server configuration
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config.yml"
        )
        
        # Default configuration
        self.config = {
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "workers": 4,
                "log_level": "info",
                "timeout": 60,
                "ssl_enabled": False,
                "ssl_cert": "",
                "ssl_key": ""
            },
            "api": {
                "enable_cors": True,
                "allowed_origins": ["*"],
                "require_api_key": False,
                "api_keys": [],
                "rate_limit_enabled": True,
                "rate_limit": 100  # requests per minute
            },
            "models": {
                "shape_analyzer_path": "models/weights/shape_analyzer_model.h5",
                "drawing_analyzer_path": "models/weights/drawing_analyzer_model.h5",
                "gaugan_model_path": "models/weights/gaugan_model.pth",
                "use_gpu": True,
                "gpu_memory_limit": 2048  # MB
            },
            "storage": {
                "type": "local",  # "local", "s3", or "azure"
                "path": "data/",
                "s3_bucket": "",
                "s3_region": "",
                "azure_container": "",
                "azure_connection_string": ""
            },
            "monitoring": {
                "enabled": True,
                "prometheus_enabled": True,
                "prometheus_port": 8001,
                "health_check_interval": 60  # seconds
            }
        }
        
        # Load configuration from file
        self.load_config()
    
    def load_config(self):
        """
        Load configuration from YAML file
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    file_config = yaml.safe_load(f)
                
                # Update configuration with file values
                self._update_nested_dict(self.config, file_config)
                logger.info(f"Loaded configuration from {self.config_path}")
            else:
                logger.warning(f"Configuration file {self.config_path} not found. Using default configuration.")
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            logger.warning("Using default configuration.")
    
    def _update_nested_dict(self, d: Dict[str, Any], u: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update nested dictionary recursively
        
        Args:
            d: Original dictionary
            u: Dictionary with updates
            
        Returns:
            Updated dictionary
        """
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                d[k] = self._update_nested_dict(d[k], v)
            else:
                d[k] = v
        return d
    
    def save_config(self, path: str = None):
        """
        Save configuration to YAML file
        
        Args:
            path: Path to save the configuration file (optional)
        """
        save_path = path or self.config_path
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Save configuration
            with open(save_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            
            logger.info(f"Saved configuration to {save_path}")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get_server_config(self) -> Dict[str, Any]:
        """
        Get server configuration
        
        Returns:
            Server configuration dictionary
        """
        return self.config["server"]
    
    def get_api_config(self) -> Dict[str, Any]:
        """
        Get API configuration
        
        Returns:
            API configuration dictionary
        """
        return self.config["api"]
    
    def get_models_config(self) -> Dict[str, Any]:
        """
        Get models configuration
        
        Returns:
            Models configuration dictionary
        """
        return self.config["models"]
    
    def get_storage_config(self) -> Dict[str, Any]:
        """
        Get storage configuration
        
        Returns:
            Storage configuration dictionary
        """
        return self.config["storage"]
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """
        Get monitoring configuration
        
        Returns:
            Monitoring configuration dictionary
        """
        return self.config["monitoring"]
    
    def get_full_config(self) -> Dict[str, Any]:
        """
        Get full configuration
        
        Returns:
            Full configuration dictionary
        """
        return self.config
    
    def override_config(self, section: str, key: str, value: Any):
        """
        Override a specific configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            value: New value
        """
        if section in self.config and key in self.config[section]:
            old_value = self.config[section][key]
            self.config[section][key] = value
            logger.info(f"Override {section}.{key}: {old_value} -> {value}")
        else:
            logger.error(f"Config key {section}.{key} not found")


def load_environment_variables(config: ServerConfig):
    """
    Override configuration with environment variables
    
    Args:
        config: ServerConfig instance
    """
    # Server settings
    if os.getenv("SERVER_HOST"):
        config.override_config("server", "host", os.getenv("SERVER_HOST"))
    
    if os.getenv("SERVER_PORT"):
        config.override_config("server", "port", int(os.getenv("SERVER_PORT")))
    
    if os.getenv("SERVER_WORKERS"):
        config.override_config("server", "workers", int(os.getenv("SERVER_WORKERS")))
    
    if os.getenv("SERVER_LOG_LEVEL"):
        config.override_config("server", "log_level", os.getenv("SERVER_LOG_LEVEL"))
    
    # API settings
    if os.getenv("API_REQUIRE_KEY"):
        config.override_config("api", "require_api_key", os.getenv("API_REQUIRE_KEY").lower() == "true")
    
    if os.getenv("API_KEYS"):
        config.override_config("api", "api_keys", os.getenv("API_KEYS").split(","))
    
    # Model settings
    if os.getenv("USE_GPU"):
        config.override_config("models", "use_gpu", os.getenv("USE_GPU").lower() == "true")
    
    if os.getenv("GPU_MEMORY_LIMIT"):
        config.override_config("models", "gpu_memory_limit", int(os.getenv("GPU_MEMORY_LIMIT")))
    
    # Storage settings
    if os.getenv("STORAGE_TYPE"):
        config.override_config("storage", "type", os.getenv("STORAGE_TYPE"))
    
    if os.getenv("S3_BUCKET"):
        config.override_config("storage", "s3_bucket", os.getenv("S3_BUCKET"))
    
    if os.getenv("S3_REGION"):
        config.override_config("storage", "s3_region", os.getenv("S3_REGION"))


def generate_default_config(output_path: str = None):
    """
    Generate a default configuration file
    
    Args:
        output_path: Path to save the configuration file (optional)
    """
    config = ServerConfig()
    config.save_config(output_path)
    logger.info("Generated default configuration")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI-PsychDoodle-Analyzer Server Configuration")
    parser.add_argument("--generate", action="store_true", help="Generate default configuration file")
    parser.add_argument("--output", help="Output path for generated configuration")
    parser.add_argument("--validate", action="store_true", help="Validate existing configuration")
    parser.add_argument("--config", help="Path to configuration file")
    
    args = parser.parse_args()
    
    if args.generate:
        generate_default_config(args.output)
    
    if args.validate:
        config_path = args.config or os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config.yml"
        )
        
        config = ServerConfig(config_path)
        logger.info("Configuration validation successful")
        logger.info(f"Server will run on {config.get_server_config()['host']}:{config.get_server_config()['port']}")
        logger.info(f"API key required: {config.get_api_config()['require_api_key']}")
        logger.info(f"Using GPU: {config.get_models_config()['use_gpu']}")