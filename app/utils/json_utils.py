import json
import jsonschema
from typing import Any, Optional, Union
import logging

import jsonschema.exceptions

class JsonUtils:
    """
    Advanced JSON validation and manipulation utilities.
    """

    @staticmethod
    def validate_json(
        data: str | dict[str, Any],
        schema: Optional[dict[str, Any]] = None
    ) -> bool:
        """
        Comprehensive JSON validation with flexible input handling

        Args:
            data: JSON data to validate (string or dictionary)
            schema: Optional JSON schema for validation

        Returns:
            Boolean indicating validation success
        """
        try:
            # Parse string input if necessary
            if isinstance(data, str):
                data = json.loads(data)
            
            # Default schema if not provided
            default_schema = {
                "type": "object",
                "properties": {
                    "data": {"type": "array"},
                    "metadata": {"type": "object"}
                }
            }

            jsonschema.validate(
                instance=data,
                schema=schema or default_schema
            )
            return True
        except (jsonschema.exceptions.ValidationError, json.JSONDecodeError) as error:
            logging.error(f"JSON validation error: {error}")
            return False
        
    @staticmethod
    def sanitize_json(
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Advanced JSON data sanitization

        Args:
            data: Input JSON data

        Returns:
            Sanitized JSON data
        """
        def _sanitize_value(value):
            """
            Recursive value sanitization
            """
            if isinstance(value, dict):
                return {
                    k: _sanitize_value(v) for k, v in value.items()
                    if not k.lower() in ["password", "secret", "token"]
                }
            elif isinstance(value, list):
                return [_sanitize_value(item) for item in value]
            elif isinstance(value, str):
                return value[:1000]
            return value
        
        return _sanitize_value(data)