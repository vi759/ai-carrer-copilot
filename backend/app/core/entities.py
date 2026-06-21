from typing import List
from pydantic import BaseModel, Field

class InterviewQuestion(BaseModel):
    question: str = Field(..., description="The interview question tailored to the candidate based on resume gaps or strengths.")
    rationale: str = Field(..., description="Explanation of why this question is being asked relative to the job requirements and resume.")
    suggested_answer: str = Field(..., description="A detailed guide or talking points on how the candidate should structure their answer.")

class LearningRoadmapMilestone(BaseModel):
    title: str = Field(..., description="A clear, actionable title for this phase of learning (e.g. 'Learn Docker Basics').")
    description: str = Field(..., description="A detailed description of the core concepts to master in this milestone.")
    resources: List[str] = Field(..., description="A list of high-quality tutorials, docs, or suggested search terms to help learn this.")

class LearningRoadmap(BaseModel):
    milestones: List[LearningRoadmapMilestone] = Field(..., description="A chronological step-by-step roadmap to acquire the missing skills.")

class ResumeSuggestion(BaseModel):
    section: str = Field(..., description="The resume section that needs improvement (e.g., 'Professional Experience', 'Skills', 'Summary').")
    suggestion: str = Field(..., description="An actionable suggestion on what to add, rephrase, or remove to better align with the job description.")

class AnalysisResult(BaseModel):
    ats_score: int = Field(..., description="An overall ATS compatibility score from 0 to 100 based on the job description match.", ge=0, le=100)
    missing_skills: List[str] = Field(..., description="Key technical or soft skills found in the job description but not in the resume.")
    skill_match_percentage: float = Field(..., description="A percentage indicating how closely the resume's skills match the job description.", ge=0.0, le=100.0)
    interview_questions: List[InterviewQuestion] = Field(..., description="A list of 3-5 custom interview questions to prepare for the role.")
    learning_roadmap: LearningRoadmap = Field(..., description="A curated roadmap to master the missing skills.")
    resume_suggestions: List[ResumeSuggestion] = Field(..., description="Tailored, actionable suggestions to make the resume stand out for this role.")
    cover_letter: str = Field(..., description="A personalized cover letter draft tailored to the job description and resume.")
