import os
import logging
from pathlib import Path
from typing import Optional

def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def validate_directory(path: str, create: bool = True) -> Path:
    """
    Validate and optionally create a directory path
    
    Args:
        path: Directory path to validate
        create: Whether to create the directory if it doesn't exist
        
    Returns:
        Path object for the validated directory
        
    Raises:
        ValueError: If path is not a directory and create=False
    """
    path_obj = Path(path)
    if not path_obj.exists():
        if create:
            path_obj.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory: {path_obj}")
        else:
            raise ValueError(f"Directory does not exist: {path_obj}")
    elif not path_obj.is_dir():
        raise ValueError(f"Path exists but is not a directory: {path_obj}")
    
    return path_obj