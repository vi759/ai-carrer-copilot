from abc import ABC, abstractmethod
from app.core.entities import AnalysisResult

class LLMGateway(ABC):
    @abstractmethod
    def analyze_resume(self, resume_text: str, job_description: str) -> AnalysisResult:
        """
        Analyze a resume text against a job description text using LLM.
        
        Args:
            resume_text (str): The plain text content of the resume.
            job_description (str): The text content of the job description.
            
        Returns:
            AnalysisResult: The structured analysis result.
            
        Raises:
            Exception: If LLM invocation or parsing fails.
        """
        pass
