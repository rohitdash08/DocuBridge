import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from typing import Optional
import os

from app.config import AppConfig
from app.core.json_to_pdf import JsonToPdfConverter
from app.core.pdf_to_json import PdfToJsonConverter

class DocuBridgeApp:
    def __init__(self, config: AppConfig):
        self.root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop support
        self.root.title("DocuBridge: JSON ↔ PDF Converter")
        self.config = config

        self._setup_ui()
        self._create_widgets()

    def _setup_ui(self):
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _create_widgets(self):
        # Conversion type selection
        conversion_frame = ttk.LabelFrame(self.root, text="Conversion Type", padding=(10, 10, 10, 0))
        conversion_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.conversion_var = tk.StringVar(value="JSON_TO_PDF")
        json_to_pdf_radio = ttk.Radiobutton(conversion_frame, text="JSON to PDF", variable=self.conversion_var, value="JSON_TO_PDF")
        pdf_to_json_radio = ttk.Radiobutton(conversion_frame, text="PDF to JSON", variable=self.conversion_var, value="PDF_TO_JSON")
        json_to_pdf_radio.pack(side="left", padx=10)
        pdf_to_json_radio.pack(side="left")

        # File selection and conversion
        file_frame = ttk.Frame(self.root)
        file_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.input_file_label = ttk.Label(file_frame, text="Input File:")
        self.input_file_label.pack(side="left", padx=(0, 10))

        self.input_file_path = tk.StringVar()
        self.input_file_entry = ttk.Entry(file_frame, textvariable=self.input_file_path, width=50)
        self.input_file_entry.pack(side="left", padx=(0, 10))

        self.input_file_button = ttk.Button(file_frame, text="Select Input File", command=self._select_input_file)
        self.input_file_button.pack(side="left", padx=(0, 10))

        self.convert_button = ttk.Button(file_frame, text="Convert", command=self._perform_conversion)
        self.convert_button.pack(side="left")

        # Conversion progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, mode="indeterminate")
        self.progress_bar.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Drag and drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self._handle_drop)

    def _select_input_file(self):
        file_types = [("JSON Files", "*.json")] if self.conversion_var.get() == "JSON_TO_PDF" else [("PDF Files", "*.pdf")]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.input_file_path.set(file_path)

    def _perform_conversion(self):
        try:
            self.progress_bar.start()
            input_path = self.input_file_path.get()
            conversion_type = self.conversion_var.get()

            if conversion_type == "JSON_TO_PDF":
                output_path = self.config.get_unique_output_path("converted_file", "pdf")
                success = JsonToPdfConverter.convert(input_path, str(output_path))
            else:
                output_path = self.config.get_unique_output_path("converted_file", "json")
                success = PdfToJsonConverter.convert(input_path, str(output_path))

            if success:
                messagebox.showinfo("Conversion Successful", f"File saved at {output_path}")
            else:
                messagebox.showerror("Conversion Failed", "Unable to complete the conversion process")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))
        finally:
            self.progress_bar.stop()

    def _handle_drop(self, event):
        file_path = event.data.strip('{').strip('}')
        self.input_file_path.set(file_path)

    def run(self):
        self.root.mainloop()
