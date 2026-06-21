from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException, status

from app.adapters.api.dependencies import get_analyze_resume_use_case
from app.adapters.api.schemas import APIAnalysisResponse, CoverLetterResponse
from app.use_cases.analyze_resume import AnalyzeResumeUseCase

router = APIRouter(
    prefix="/api/v1",
    tags=["Analysis"]
)


@router.post("/analyze", response_model=APIAnalysisResponse)
async def analyze_resume_endpoint(
    resume: UploadFile = File(..., description="Upload Resume in PDF format"),
    job_description: str = Form(..., description="Paste target Job Description text here"),
    use_case: AnalyzeResumeUseCase = Depends(get_analyze_resume_use_case)
):
    filename = resume.filename or ""

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF resumes are supported."
        )

    try:
        pdf_bytes = await resume.read()

        analysis_result = use_case.execute(
            pdf_bytes,
            job_description
        )

        return analysis_result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/cover-letter", response_model=CoverLetterResponse)
async def generate_cover_letter_endpoint(
    resume: UploadFile = File(..., description="Upload Resume in PDF format"),
    job_description: str = Form(..., description="Paste target Job Description text here"),
    use_case: AnalyzeResumeUseCase = Depends(get_analyze_resume_use_case)
):
    filename = resume.filename or ""

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF resumes are supported."
        )

    try:
        pdf_bytes = await resume.read()

        analysis_result = use_case.execute(
            pdf_bytes,
            job_description
        )

        return CoverLetterResponse(
            cover_letter=analysis_result.cover_letter
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )