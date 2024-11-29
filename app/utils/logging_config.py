import logging
import structlog
from pathlib import Path
from typing import Optional

class LoggingConfig:
    """
    Centralized logging configuration with structured logging.
    """
    @staticmethod
    def configure_logging(
        log_dir: Optional[Path] = None,
        log_level: int = logging.INFO
    ) -> structlog.BoundLogger:
        """
        Configure structured logging with file and console outputs

        Args:
            log_dir: directory for log files
            log_level: logging verbosity level
        
        Returns:
            Configured structured logger
        """

        # Logging configuration
        logging.basicConfig(
            level=log_level,
            format='%(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(
                    filename=(log_dir or Path.cwd()) / 'docubridge.log',
                )
            ]
        )

        # Structured logging configuration
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger()