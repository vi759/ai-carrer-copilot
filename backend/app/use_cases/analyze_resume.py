from app.use_cases.ports.pdf_parser import PDFParser
from app.core.entities import (
    AnalysisResult,
    ResumeSuggestion,
    LearningRoadmap,
    LearningRoadmapMilestone,
    InterviewQuestion
)


class AnalyzeResumeUseCase:

    def __init__(self, pdf_parser: PDFParser, llm_gateway=None):
        self.pdf_parser = pdf_parser

    def execute(self, resume_bytes: bytes, job_description: str) -> AnalysisResult:

        if not resume_bytes:
            raise ValueError("Resume file cannot be empty.")

        if not job_description.strip():
            raise ValueError("Job description cannot be empty.")

        resume_text = self.pdf_parser.extract_text(resume_bytes)

        if not resume_text.strip():
            raise ValueError(
                "Could not extract any readable text from the uploaded PDF resume."
            )

        skills = [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "statistics",
        "data analysis",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "nlp",
        "computer vision",
        "fastapi",
        "flask",
        "django",
        "html",
        "css",
        "javascript",
        "react",
        "nodejs",
        "git",
        "github",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "mongodb",
        "mysql",
        "postgresql",
        "spark",
        "hadoop",
        "xgboost",
        "random forest",
        "rag",
        "llm",
        "langchain",
        "genai",
        "openai",
        "hugging face",
        "streamlit",
        "power query",
        "dax",
        "eda"]

        resume_lower = resume_text.lower()
        jd_lower = job_description.lower()

        resume_skills = [
            skill for skill in skills
            if skill in resume_lower
        ]

        jd_skills = [
            skill for skill in skills
            if skill in jd_lower
        ]

        matched_skills = list(
            set(resume_skills).intersection(set(jd_skills))
        )

        missing_skills = list(
            set(jd_skills) - set(resume_skills)
        )

        # Calculate Skill Match %

        matched_count = len(matched_skills)
        jd_count = max(len(jd_skills), 1)
        resume_count = len(resume_skills)

        skill_match_percentage = round(
            (matched_count / jd_count) * 100,
            2
        )

        # Better ATS Score Formula

        ats_score = round(
            (
                skill_match_percentage * 0.75
            ) +
            (
                min(resume_count, 20) * 1.25
            )
        )

        if ats_score > 100:
            ats_score = 100

        if ats_score < 0:
            ats_score = 0

        resume_suggestions = [
            ResumeSuggestion(
                section="Projects",
                suggestion="Add quantified project achievements."
            ),
            ResumeSuggestion(
                section="Experience",
                suggestion="Use action verbs and measurable outcomes."
            )
        ]

        for skill in missing_skills[:5]:
            resume_suggestions.append(
                ResumeSuggestion(
                    section="Skills",
                    suggestion=f"Add {skill} if you have experience with it."
                )
            )

        milestones = []

        for skill in missing_skills[:5]:
            milestones.append(
                LearningRoadmapMilestone(
                    title=f"Learn {skill}",
                    description=f"Gain practical experience in {skill}",
                    resources=[
                        "YouTube",
                        "Coursera",
                        "Official Documentation"
                    ]
                )
            )

        learning_roadmap = LearningRoadmap(
            milestones=milestones
        )

        interview_questions = []

        for skill in missing_skills[:5]:
            interview_questions.append(
                InterviewQuestion(
                    question=f"Explain your experience with {skill}.",
                    rationale=f"{skill} appears in the job description.",
                    suggested_answer=f"Prepare practical examples involving {skill}."
                )
            )

        cover_letter = f"""
Dear Hiring Manager,

I am excited to apply for this opportunity.

My background includes experience with:
{', '.join(matched_skills) if matched_skills else 'relevant technical skills'}.

Thank you for your consideration.

Sincerely,
Candidate
"""

        return AnalysisResult(
            ats_score=ats_score,
            missing_skills=missing_skills,
            skill_match_percentage=skill_match_percentage,
            interview_questions=interview_questions,
            learning_roadmap=learning_roadmap,
            resume_suggestions=resume_suggestions,
            cover_letter=cover_letter
        )