import pytest
from fastapi.testclient import TestClient
from app.adapters.api.main import app
from app.adapters.api.dependencies import get_llm_gateway, get_pdf_parser
from app.use_cases.ports.pdf_parser import PDFParser
from app.use_cases.ports.llm_gateway import LLMGateway
from app.core.entities import AnalysisResult, InterviewQuestion, LearningRoadmap, LearningRoadmapMilestone, ResumeSuggestion

# ----------------------------------------------------
# Mock Implementations for Isolation Testing
# ----------------------------------------------------

class MockPDFParser(PDFParser):
    def extract_text(self, file_bytes: bytes) -> str:
        return "Experienced Software Engineer skilled in Python, FastAPI, and Docker."

class MockLLMGateway(LLMGateway):
    def analyze_resume(self, resume_text: str, job_description: str) -> AnalysisResult:
        return AnalysisResult(
            ats_score=85,
            missing_skills=["Kubernetes", "GraphQL", "CI/CD Pipelines"],
            skill_match_percentage=78.5,
            interview_questions=[
                InterviewQuestion(
                    question="Can you explain your experience containerizing FastAPI applications?",
                    rationale="The job description requires Docker/Kubernetes, and your resume lists Docker.",
                    suggested_answer="Focus on multi-stage Docker builds, health checks, and running behind an ASGI server like Uvicorn."
                )
            ],
            learning_roadmap=LearningRoadmap(
                milestones=[
                    LearningRoadmapMilestone(
                        title="Master Kubernetes Orchestration",
                        description="Learn core Kubernetes concepts including Pods, Services, and Deployments.",
                        resources=["Kubernetes Documentation", "KubeAcademy by VMware"]
                    )
                ]
            ),
            resume_suggestions=[
                ResumeSuggestion(
                    section="Work Experience",
                    suggestion="Incorporate more quantitative results. E.g., 'Containerized backend reducing deployment latency by 20%'."
                )
            ],
            cover_letter="Dear Hiring Team,\n\nI am excited to apply for the role because my experience with Python, FastAPI, and Docker aligns closely with the requirements. I have a proven record of building scalable backend services and containerized delivery pipelines. I look forward to contributing strong technical leadership and a passion for continuous improvement to your team.\n\nSincerely,\nCandidate"
        )

# Override FastAPI dependencies with our mocks
app.dependency_overrides[get_pdf_parser] = lambda: MockPDFParser()
app.dependency_overrides[get_llm_gateway] = lambda: MockLLMGateway()

client = TestClient(app)

# ----------------------------------------------------
# Test Cases
# ----------------------------------------------------

def test_analyze_endpoint_success():
    """Verify that a successful upload of a PDF and job description returns correct JSON structure."""
    dummy_pdf_bytes = b"%PDF-1.4 dummy resume content"
    
    response = client.post(
        "/api/v1/analyze",
        files={"resume": ("my_resume.pdf", dummy_pdf_bytes, "application/pdf")},
        data={"job_description": "FastAPI Developer with Kubernetes experience."}
    )
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Assert values from mock gateway
    assert json_response["ats_score"] == 85
    assert json_response["skill_match_percentage"] == 78.5
    assert "Kubernetes" in json_response["missing_skills"]
    assert len(json_response["interview_questions"]) == 1
    assert json_response["interview_questions"][0]["question"] == "Can you explain your experience containerizing FastAPI applications?"
    assert len(json_response["learning_roadmap"]["milestones"]) == 1
    assert json_response["resume_suggestions"][0]["section"] == "Work Experience"

def test_analyze_endpoint_invalid_file():
    """Verify endpoint rejects non-PDF file extensions with 400 Bad Request."""
    response = client.post(
        "/api/v1/analyze",
        files={"resume": ("resume.txt", b"plain text resume content", "text/plain")},
        data={"job_description": "FastAPI Developer"}
    )
    
    assert response.status_code == 400
    assert "Only PDF resumes are supported" in response.json()["detail"]


def test_cover_letter_endpoint_success():
    """Verify that the cover letter endpoint returns a personalized draft."""
    dummy_pdf_bytes = b"%PDF-1.4 dummy resume content"

    response = client.post(
        "/api/v1/cover-letter",
        files={"resume": ("my_resume.pdf", dummy_pdf_bytes, "application/pdf")},
        data={"job_description": "FastAPI Developer with Kubernetes experience."}
    )

    assert response.status_code == 200
    json_response = response.json()
    assert "cover_letter" in json_response
    assert "Dear Hiring Team" in json_response["cover_letter"]


def test_analyze_endpoint_missing_fields():
    """Verify endpoint rejects request if job description is missing."""
    dummy_pdf_bytes = b"%PDF-1.4 dummy resume content"
    
    # Request without job_description
    response = client.post(
        "/api/v1/analyze",
        files={"resume": ("my_resume.pdf", dummy_pdf_bytes, "application/pdf")},
        data={}
    )
    
    assert response.status_code == 422 # Validation Error (missing form field)
