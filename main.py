import sys
from typing import Optional
import logging

from app.gui.app_ui import DocuBridgeApp
from app.config import AppConfig
from app.utils.logging_config import LoggingConfig

def main() -> Optional[int]:
    """
    Main entry point for DocuBridge application.
    Initializes logging, configuration and launches the GUI.

    Returns:
        Optional exit code for the application.
    """
    try:
        # Setup Logging configuration
        logger = LoggingConfig.configure_logging()
        logger.info("DocuBridge application starting...")

        # Load application configuration
        config = AppConfig()

        # Initialize and run the main application
        app = DocuBridgeApp(config)
        app.run()

        return 0
    except Exception as e:
        logging.error(f"Unhandled application error: {e}", exc_info=True)
        return 1
    
if __name__ == "__main__":
    sys.exit(main())