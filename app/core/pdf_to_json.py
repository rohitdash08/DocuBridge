import json
from typing import Any, Optional
import logging

from app.utils.pdf_utils import PdfUtils

class PdfToJsonConverter:
    """
    Advanced PDF to JSON extraction with intelligent parsing.
    """
    @classmethod
    def convert(
        cls,
        pdf_path: str,
        output_path: str,
        extraction_strategy: Optional[str] = None
    ) -> bool:
        """
        Comprehensive PDF to JSON conversion

        Args:
            pdf_path: Source PDF file path
            output_path: Destination JSON file path
            extraction_strategy: Optional custom extraction method

        Returns:
            Boolean indicating successful conversion
        """
        try:
            # Extract text from PDF
            extracted_data = PdfUtils.extract_text_from_pdf(pdf_path)

            # Apply custom extraction strategy if provided
            if extraction_strategy:
                extracted_data = cls._apply_extraction_strategy(
                    extracted_data,
                    extraction_strategy
                )

            # Write to JSON
            with open(output_path, "w", encoding="utf-8") as json_file:
                json.dump(extracted_data, json_file, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            logging.error(f"PDF to JSON conversion error: {e}")
            return False
    
    @staticmethod
    def _apply_extraction_strategy(
        data: dict[str, Any],
        strategy: str
    ) -> dict[str, Any]:
        """
        Apply custom extraction strategy to data

        Args:
            data: extracted PDF data
            strategy: extraction strategy name

        Returns:
            Processed data
        """
        strategies = {
            "clean_text": lambda d: {
                **d,
                "pages": [
                    {**page, "content": page["content"].strip()}
                    for page in d.get("pages", [])
                ]
            },
            "extract_paragraphs": lambda d: {
                **d,
                "pages": [
                    {**page, "paragraphs": page["content"].split("\n\n")}
                    for page in d.get("pages", [])
                ]
            }
        }

        return strategies.get(strategy, lambda x: x)(data)