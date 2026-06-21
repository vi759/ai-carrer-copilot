import json
from typing import Any

import google.genai as genai
from app.core.entities import AnalysisResult
from app.core.config import settings
from app.use_cases.ports.llm_gateway import LLMGateway


class GeminiGateway(LLMGateway):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.google_api_key
        self.model = model or settings.gemini_model

        if not self.api_key:
            raise RuntimeError(
                "Gemini API key is not configured. Set GOOGLE_API_KEY in .env or the environment."
            )

        self.client = genai.Client(api_key=self.api_key)

    def analyze_resume(
        self,
        resume_text: str,
        job_description: str
    ) -> AnalysisResult:

        prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the resume against the job description.

Return ONLY valid JSON.

JSON Format:

{{
  "ats_score": 85,
  "skill_match_percentage": 80,
  "missing_skills": ["Skill1", "Skill2"],
  "resume_suggestions": [
    {{
      "section": "Skills",
      "suggestion": "Add Machine Learning projects"
    }}
  ],
  "learning_roadmap": {{
    "milestones": [
      {{
        "title": "Learn Python",
        "description": "Master Python fundamentals",
        "resources": ["Python Docs"]
      }}
    ]
  }},
  "interview_questions": [
    {{
      "question": "What is Machine Learning?",
      "rationale": "Tests fundamentals",
      "suggested_answer": "Machine Learning is..."
    }}
  ],
  "cover_letter": "Generated cover letter here"
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        raw_text = response.text

        json_text = self._extract_json_fragment(raw_text)

        parsed = self._parse_json(json_text)

        return AnalysisResult.model_validate(parsed)

    def _extract_json_fragment(self, raw_text: str) -> str:
        raw_text = raw_text.strip()

        if raw_text.startswith("{") and raw_text.endswith("}"):
            return raw_text

        start = None
        depth = 0

        for index, char in enumerate(raw_text):
            if char == "{":
                if depth == 0:
                    start = index
                depth += 1

            elif char == "}":
                depth -= 1

                if depth == 0 and start is not None:
                    return raw_text[start:index + 1]

        raise RuntimeError(
            "Unable to extract JSON from Gemini response:\n"
            + raw_text
        )

    def _parse_json(self, json_text: str) -> dict[str, Any]:
        try:
            return json.loads(json_text)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Failed to parse Gemini JSON response: {exc}"
            ) from exc