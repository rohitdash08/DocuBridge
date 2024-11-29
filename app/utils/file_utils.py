from typing import Optional
from pathlib import Path
import os
import logging

class FileUtils:
    """
    Centralized file validation and utility methods.
    """

    @staticmethod
    def validate_file_size(file_path: Path, max_size_mb: int = 100) -> bool:
        """
        Validate file size against maximum allowed size.

        Args:
            file_path: Path to the file
            max_size_mb: Maximum allowed file size in megabytes

        Returns:
            Boolean indicating file size validity
        """
        try:
            file_size = os.path.getsize(file_path) / (1024 * 1024) # Convert to MB
            return 0 < file_size <= max_size_mb
        except Exception as e:
            logging.error(f"File size validation error: {e}")
            return False
    
    @staticmethod
    def get_valid_files(
        directory: Path,
        valid_extensions: list[str],
    ) -> list[Path]:
        """
        Retrieve valid files from a directory

        Args:
            directory: Directory to scan
            valid_extensions: List of valid file extensions

        Returns:
            list of valid file paths
        """
        return [
            file for file in directory.iterdir()
            if file.is_file() and file.suffix.lstrip(".") in valid_extensions
        ]