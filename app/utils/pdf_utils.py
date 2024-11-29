import pdfplumber
from typing import Any
import logging

class PdfUtils:
    """
    Advanced PDF parsing utilities.
    """
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> dict[str, Any]:
        """
        Intelligent PDF text extraction with structured output

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                extracted_data = {
                    "metadata": {
                        "total_pages": len(pdf.pages),
                        "file_path": pdf_path
                    },
                    "pages": []
                }

                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    extracted_data["pages"].append({
                        "page_number": page_num,
                        "context": page_text.strip() if page_text else ""
                    })
                
                return extracted_data
        except Exception as e:
            logging.error(f"PDF text extraction error: {e}")
            return {}
        
    @staticmethod
    def get_pdf_page_count(pdf_path: str) -> int:
        """
        Retrieve total number of pages in a PDF

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Number of pages in the PDF
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages)
        except Exception as e:
            logging.error(f"PDF page count error: {e}")
            return 0