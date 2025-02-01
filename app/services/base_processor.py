# app/services/base_processor.py
from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """Extract text from the given file."""
        pass
