import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from app.config import AppConfig
from app.core.json_to_pdf import JsonToPdfConverter
from app.core.pdf_to_json import PdfToJsonConverter
from app.utils.file_utils import FileUtils

class DocuBridgeApp:
    """
    Main application GUI with conversion capabilities.
    """
    def __init__(self, config: AppConfig):
        self.root = tk.Tk()
        self.root.title("DocuBridge: JSON ↔ PDF Converter")
        self.config = config

        self._setup_ui()
        self._create_widgets()

    def _setup_ui(self):
        """
        Configure UI Layout and styling
        """
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

    def _create_widgets(self):
        """
        Create and layout application widgets
        """
        # Conversion type selection
        self.conversion_var = tk.StringVar(value="JSON_TO_PDF")
        conversion_frame = ttk.LabelFrame(self.root, text="Conversion Type")
        conversion_frame.pack(padx=10, pady=10, fill="x")

        json_to_pdf_radio = ttk.Radiobutton(
            conversion_frame,
            text="JSON to PDF",
            variable=self.conversion_var,
            value="JSON_TO_PDF",
        )

        pdf_to_json_radio = ttk.Radiobutton(
            conversion_frame,
            text="PDF to JSON",
            variable=self.conversion_var,
            value="PDF_TO_JSON",
        )
        json_to_pdf_radio.pack(side="left", padx=10)
        pdf_to_json_radio.pack(side="left")

        # File selection buttons
        file_frame = ttk.Frame(self.root)
        file_frame.pack(padx=10, pady=10)

        self.input_file_button = ttk.Button(
            file_frame,
            text="Select Input File",
            command=self._select_input_file
        )
        self.input_file_button.pack(side="left", padx=5)

    def _select_input_file(self):
        """
        Handle input file selection based on conversion type
        """
        conversion_type = self.conversion_var.get()

        if conversion_type == "JSON_TO_PDF":
            file_types = [("JSON Files", "*.json")]
            conversion_method = self._convert_json_to_pdf
        else:
            file_types = [("PDF Files", "*.pdf")]
            conversion_method = self._convert_pdf_to_json
        
        file_path = filedialog.askopenfilename(filetypes=file_types)

        if file_path:
            self._perform_conversion(file_path, conversion_method)

    def _perform_conversion(self, input_path, conversion_method):
        """
        Execute conversion and handle result
        """
        try:
            output_path = self.config.get_unique_output_path(
                "converted_file",
                "pdf" if conversion_method == self._convert_json_to_pdf else "json"
            )
            success = conversion_method(input_path, str(output_path))

            if success:
                messagebox.showinfo(
                    "Conversion Successful",
                    f"File saved at {output_path}"
                )
            else:
                messagebox.showerror(
                    "Conversion Failed",
                    "Unable to complete the conversion process"
                )
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def _convert_json_to_pdf(
            self,
            input_path: str,
            output_path: str
    ) -> bool:
        """JSON to PDF conversion wrapper"""
        return JsonToPdfConverter.convert(input_path, output_path)
    
    def _convert_pdf_to_json(
            self,
            input_path: str,
            output_path: str
    ) -> bool:
        """PDF to JSON conversion wrapper"""
        return PdfToJsonConverter.convert(input_path, output_path)
    
    def run(self):
        """
        Start the application event loop
        """
        self.root.mainloop() # Start the tkinter event loop

        