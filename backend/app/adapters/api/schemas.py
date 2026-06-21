from pydantic import BaseModel
from app.core.entities import AnalysisResult

class CoverLetterResponse(BaseModel):
    cover_letter: str

# We can directly use the domain's AnalysisResult entity as the response schema.
# In a larger application, we might map domain entities to API-specific schemas,
# but for our use case, they align perfectly.
APIAnalysisResponse = AnalysisResult
