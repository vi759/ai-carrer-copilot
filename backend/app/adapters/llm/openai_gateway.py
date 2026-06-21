from openai import OpenAI
from app.use_cases.ports.llm_gateway import LLMGateway
from app.core.entities import AnalysisResult
from app.core.config import settings

class OpenAIGateway(LLMGateway):
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model
        
        # Initialize OpenAI client. If api_key is None or empty, OpenAI client
        # will look up the OPENAI_API_KEY environment variable.
        client_kwargs = {}
        if self.api_key:
            client_kwargs["api_key"] = self.api_key
            
        self.client = OpenAI(**client_kwargs)

    def analyze_resume(self, resume_text: str, job_description: str) -> AnalysisResult:
        """
        Calls OpenAI Chat Completion API to compare the resume text with the job description
        and parses the response directly into the AnalysisResult Pydantic schema.
        """
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert technical recruiter, talent manager, and career coach.\n"
                            "Your job is to objectively analyze the provided Resume text against the Job Description text.\n"
                            "Return a structured evaluation that includes:\n"
                            "1. An realistic ATS score (0 to 100) indicating how well the candidate aligns with the requirements.\n"
                            "2. An list of missing skills or keywords that are crucial for the job description but omitted/weak in the resume.\n"
                            "3. A skill match percentage (0 to 100).\n"
                            "4. A list of 3-5 tailored interview questions with rationales and detailed suggested answers.\n"
                            "5. A step-by-step learning roadmap of milestones with resource lists to master the missing skills.\n"
                            "6. Bulleted suggestions on how the candidate can optimize or rewrite their resume for this job.\n\n"
                            "Be professional, accurate, and constructive."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"### RESUME TEXT:\n{resume_text}\n\n### JOB DESCRIPTION:\n{job_description}"
                    }
                ],
                response_format=AnalysisResult,
            )
            
            parsed_result = response.choices[0].message.parsed
            if parsed_result is None:
                # Fallback if parsing didn't complete correctly
                refuse = getattr(response.choices[0].message, 'refusal', None)
                if refuse:
                    raise RuntimeError(f"OpenAI refused to output structured result: {refuse}")
                raise RuntimeError("Failed to parse response into AnalysisResult schema.")
                
            return parsed_result
        except Exception as e:
            raise RuntimeError(f"Failed to analyze resume with OpenAI: {str(e)}") from e
