import fitz
from app.use_cases.ports.pdf_parser import PDFParser

class PyMuPDFParser(PDFParser):
    def extract_text(self, file_bytes: bytes) -> str:
        """
        Extracts plain text from raw PDF file bytes using PyMuPDF (fitz).
        """
        try:
            text_parts = []
            # Open PDF from byte stream
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                for page in doc:
                    page_text = page.get_text()
                    if page_text:
                        text_parts.append(page_text)
            
            return "\n".join(text_parts)
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF using PyMuPDF: {str(e)}") from e
