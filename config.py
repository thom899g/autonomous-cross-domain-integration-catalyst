"""
Configuration and constants for the Cross-Domain Integration Engine.
Uses Pydantic for validation to ensure all required environment variables are present.
"""
import os
from typing import Dict, List, Optional
from pydantic import BaseSettings, Field, validator
from pathlib import Path
import logging

class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Firebase Configuration
    firebase_credentials_path: str = Field(
        default="/path/to/serviceAccountKey.json",
        description="Path to Firebase service account credentials"
    )
    firebase_project_id: str = Field(
        default="your-project-id",
        description="Firebase project ID"
    )
    
    # API Configuration
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key for advanced analysis"
    )
    
    # Path Configuration
    knowledge_base_path: str = Field(
        default="./knowledge_base",
        description="Path to store knowledge base files"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    # System Configuration
    max_workers: int = Field(
        default=4,
        description="Maximum number of worker threads"
    )
    max_concurrent_requests: int = Field(
        default=10,
        description="Maximum concurrent API requests"
    )
    
    # Domain Configuration
    default_domains: List[str] = Field(
        default=[
            "machine_learning",
            "systems_biology", 
            "quantum_computing",
            "materials_science",
            "cognitive_psychology",
            "financial_modeling"
        ],
        description="Default domains to analyze"
    )
    
    # Performance Thresholds
    similarity_threshold: float = Field(
        default=0.65,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for domain connection"
    )
    confidence_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum confidence for integration suggestions"
    )
    
    @validator('knowledge_base_path')
    def validate_knowledge_base_path(cls, v):
        """Ensure knowledge base path exists"""
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level string"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

# Global settings instance
settings = Settings()

# Configure logging
def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('integration_engine.log')
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()