#!/usr/bin/env python3
"""
Configuration file for CV Customization System
"""

import os
from typing import Optional


class Config:
    """Configuration class for CV Customization System."""

    # API Configuration
    LLM_API_KEY: Optional[str] = os.getenv("LLM_API_KEY")
    LLM_API_ENDPOINT: str = os.getenv(
        "LLM_API_ENDPOINT", "https://api.openai.com/v1/chat/completions"
    )
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))

    # Document Configuration
    DEFAULT_OUTPUT_DIR: str = os.getenv("DEFAULT_OUTPUT_DIR", ".")
    DOCUMENT_MARGINS = {"top": 0.5, "bottom": 0.5, "left": 0.75, "right": 0.75}

    # CV Sections to customize
    CUSTOMIZABLE_SECTIONS = ["summary", "achievements"]

    # File extensions
    SUPPORTED_TEMPLATE_FORMATS = [".yaml", ".yml"]
    SUPPORTED_JOB_DESCRIPTION_FORMATS = [".txt", ".md"]
    OUTPUT_FORMAT = ".docx"

    @classmethod
    def validate_api_config(cls) -> bool:
        """Validate that API configuration is complete."""
        if not cls.LLM_API_KEY:
            print(
                "Warning: LLM_API_KEY not set. Set environment variable or pass --api-key"
            )
            return False
        return True

    @classmethod
    def get_api_config(cls) -> dict:
        """Get API configuration as dictionary."""
        return {
            "api_key": cls.LLM_API_KEY,
            "api_endpoint": cls.LLM_API_ENDPOINT,
            "model": cls.LLM_MODEL,
            "temperature": cls.LLM_TEMPERATURE,
            "max_tokens": cls.LLM_MAX_TOKENS,
        }
