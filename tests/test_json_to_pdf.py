import pytest
from pathlib import Path
from app.core.json_to_pdf import JsonToPdfConverter

class TestJsonToPdfConverter:
    """
    Comprehensive test suite for JSON to PDF conversion
    """
    @pytest.fixture
    def sample_json_data(self):
        return {
            "name": "DocuBridge Test",
            "version": "1.0.0",
            "features": ["JSON Conversion", "PDF Generation"]
        }

    def test_successful_conversion(self, sample_json_data, tmp_path):
        """
        Test successful JSON to PDF conversion
        """
        output_path = tmp_path / "test_output.pdf"
        result = JsonToPdfConverter.convert(sample_json_data, str(output_path))
        
        assert result is True
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_empty_json_conversion(self, tmp_path):
        """
        Test conversion with empty JSON data
        """
        output_path = tmp_path / "empty_output.pdf"
        result = JsonToPdfConverter.convert({}, str(output_path))
        
        assert result is False