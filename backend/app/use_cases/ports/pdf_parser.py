from abc import ABC, abstractmethod

class PDFParser(ABC):
    @abstractmethod
    def extract_text(self, file_bytes: bytes) -> str:
        """
        Extract plain text content from PDF file bytes.
        
        Args:
            file_bytes (bytes): The raw binary bytes of the PDF file.
            
        Returns:
            str: The extracted plain text.
            
        Raises:
            Exception: If parsing fails or is invalid.
        """
        pass
