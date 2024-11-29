from typing import Any
import json
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


class JsonToPdfConverter:
    """
    Advanced JSON to PDF conversion with robust error handling.
    """
    @classmethod
    def convert(
        cls,
        data: str | dict[str, Any],
        output_path: str
    ) -> bool:
        """
        Comprehensive JSON to PDF conversion

        Args:
            data: JSON data (string or dictionary)
            output_path: Destination PDF file path

        Returns:
            Boolean indicating successful conversion
        """
        try:
            # Parse string input if necessary
            if isinstance(data, str):
                data = json.loads(data)

            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            elements = []

            # get styles
            styles = getSampleStyleSheet()

            # Flatten and process JSON
            flattened_data = cls._flatten_json(data)

            # Create table data
            table_data = [["Key", "Value"]]
            table_data.extend([
                [str(key), str(value)]
                for key, value in flattened_data.items()
            ])

            # Create table with styling
            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 12),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,1), (-1,-1), 10),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))

            elements.append(table)

            # Build PDF
            doc.build(elements)

            return True
        except Exception as e:
            logging.error(f"JSON to PDF conversion error: {e}")
            return False
        
    @staticmethod
    def _flatten_json(
        data: dict[str, Any],
        parent_key: str = "",
        sep: str = "."
    ) -> dict[str, str]:
        """
        Recursive JSON flattening with advanced handling

        Args:
            data: JSON data to flatten
            parent_key: Parent key for nested structures
            sep: Separator for nested keys
        
        Returns:
            Flattened dictionary
        """

        items = {}

        def _flatten(x, name=""):
            if isinstance(x, dict):
                for k, v in x.items():
                    _flatten(v, f"{name}{k}{sep}")
            elif isinstance(x, list):
                for i, v in enumerate(x):
                    _flatten(v, f"{name}{i}{sep}")
            else:
                items[name[:-1]] = str(x)

        _flatten(data)
        return items