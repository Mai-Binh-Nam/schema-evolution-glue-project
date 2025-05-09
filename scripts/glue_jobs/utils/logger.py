import logging
import sys
from datetime import datetime

def setup_logging(log_level=logging.INFO):
    """
    Set up a logger for Glue jobs with appropriate formatting
    
    Args:
        log_level: The logging level (default: INFO)
        
    Returns:
        A configured logger instance
    """
    # Create logger
    logger = logging.getLogger('glue_schema_evolution')
    logger.setLevel(log_level)
    
    # Prevent adding handlers multiple times
    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add formatter to handler
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger

def log_job_metrics(logger, metrics_dict):
    """
    Log job metrics in a structured format
    
    Args:
        logger: The logger instance
        metrics_dict: Dictionary containing job metrics
    """
    logger.info(f"JOB METRICS: {datetime.now().isoformat()}")
    for key, value in metrics_dict.items():
        logger.info(f"  {key}: {value}")
