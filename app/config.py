from dataclasses import dataclass, field
from pathlib import Path
import os

@dataclass
class AppConfig:
    """
    Centralized configuration management for DocuBridge.
    Provides a single source of truth for application settings.
    """
    base_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    log_dir: Path = field(init=False)
    output_dir: Path = field(init=False)

    max_file_size_mb: int = 100
    supported_extenstions: dict[str, list[str]] = field(default_factory=lambda: {
        "json": ["json", "jsonl"],
        "pdf": ["pdf", "pdfa"]
    })

    def __post_init__(self):
        """
        Initialize derived paths and ensure directory existence.
        """
        self.log_dir = self.base_dir / "logs"
        self.output_dir = self.base_dir / "output"

        # Create necessary directories
        for directory in [self.log_dir, self.output_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def get_unique_output_path(self, filename: str, extension: str) -> Path:
        """
        Generate a unique output file path

        Args:
            filename: Base filename
            extension: File extension

        Returns:
            Unique file path
        """
        counter = 1
        output_path = self.output_dir / f"{filename}.{extension}"

        while output_path.exists():
            output_path = self.output_dir / f"{filename}_{counter}.{extension}"
            counter += 1

        return output_path
