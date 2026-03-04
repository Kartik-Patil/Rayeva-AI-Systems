"""
Structured logging service for Rayeva AI Systems.
Provides JSON logging with rotation and module-specific loggers.
"""
import logging
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from logging.handlers import RotatingFileHandler

from .config import settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        
        # Add extra fields if present
        if hasattr(record, "data"):
            log_data["data"] = record.data
        
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class LoggingService:
    """Service for managing structured logging across modules."""
    
    def __init__(self):
        self.log_dir = Path(settings.log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self._loggers: Dict[str, logging.Logger] = {}
    
    def get_logger(self, module_name: str) -> logging.Logger:
        """
        Get or create a logger for a specific module.
        
        Args:
            module_name: Name of the module (e.g., 'category_tagger')
            
        Returns:
            Configured logger instance
        """
        if module_name in self._loggers:
            return self._loggers[module_name]
        
        logger = logging.getLogger(module_name)
        logger.setLevel(getattr(logging, settings.log_level.upper()))
        logger.propagate = False
        
        # Console handler (human-readable)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler (JSON format with rotation)
        log_file = self.log_dir / f"{module_name}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=settings.log_retention_days
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(JSONFormatter())
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        self._loggers[module_name] = logger
        return logger
    
    def log_ai_interaction(
        self,
        module: str,
        prompt: str,
        response: Dict[str, Any],
        tokens_used: int,
        processing_time_ms: int,
        error: Optional[str] = None
    ):
        """
        Log AI interaction with structured data.
        
        Args:
            module: Module name
            prompt: AI prompt sent
            response: AI response received
            tokens_used: Number of tokens consumed
            processing_time_ms: Processing time in milliseconds
            error: Error message if any
        """
        logger = self.get_logger("ai_interactions")
        
        log_data = {
            "module": module,
            "prompt_length": len(prompt),
            "tokens_used": tokens_used,
            "processing_time_ms": processing_time_ms,
            "model": settings.ai_model,
            "success": error is None
        }
        
        if error:
            log_data["error"] = error
        
        logger.info(
            f"AI interaction for {module}",
            extra={"data": log_data}
        )


# Global logging service instance
logging_service = LoggingService()
