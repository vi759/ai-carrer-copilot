from fastapi import Depends
from app.adapters.pdf.pymupdf_parser import PyMuPDFParser
from app.adapters.llm.gemini_gateway import GeminiGateway
from app.use_cases.analyze_resume import AnalyzeResumeUseCase
from app.use_cases.ports.pdf_parser import PDFParser
from app.use_cases.ports.llm_gateway import LLMGateway

def get_pdf_parser() -> PDFParser:
    """Dependency provider for the PDFParser interface."""
    return PyMuPDFParser()

from app.adapters.llm.gemini_gateway import GeminiGateway

def get_llm_gateway():
    return GeminiGateway()

def get_analyze_resume_use_case(
    pdf_parser: PDFParser = Depends(get_pdf_parser),
    llm_gateway: LLMGateway = Depends(get_llm_gateway)
) -> AnalyzeResumeUseCase:
    """Dependency provider for the AnalyzeResumeUseCase interactor."""
    return AnalyzeResumeUseCase(pdf_parser=pdf_parser, llm_gateway=llm_gateway)

