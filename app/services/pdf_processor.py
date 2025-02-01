import pdfplumber

from app.services.base_processor import BaseProcessor

class PDFProcessor(BaseProcessor):
    def extract_text(self, file_path: str) -> str:
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            raise ValueError(f"Error processing PDF: {e}")
