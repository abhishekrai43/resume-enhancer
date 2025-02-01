# app/services/docx_processor.py
from docx import Document
from app.services.base_processor import BaseProcessor

class DOCXProcessor(BaseProcessor):
    def extract_text(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
            return text
        except Exception as e:
            raise ValueError(f"Error processing DOCX: {e}")
