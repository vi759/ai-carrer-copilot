# AI Career Copilot

A modern web application to help job seekers improve their chances by analyzing resume PDFs against job descriptions, generating ATS scores, identifying missing skills, providing personalized learning roadmaps, tailored interview questions, and a cover letter draft.

## Tech Stack
- FastAPI backend
- HTML / CSS / JavaScript frontend
- Gemini API via `google.genai`
- PyMuPDF for PDF parsing

## Setup
1. Create a Python virtual environment in `backend`:
   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Copy the example environment file:
   ```powershell
   copy .env.example .env
   ```
3. Add your Gemini API key to `backend/.env`:
   ```text
   GOOGLE_API_KEY=your_gemini_api_key_here
   GOOGLE_MODEL=gemini-1.5-flash
   ```
4. Run the backend server:
   ```powershell
   uvicorn app.adapters.api.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Open `frontend/index.html` in your browser or serve it with any static server.

## Features
- Upload resume PDF
- Paste job description
- ATS score analysis
- Skill match percentage
- Missing skills detection
- Resume improvement suggestions
- Personalized learning roadmap
- Interview question generation
- Cover letter draft generation

## Notes
- Backend reads `backend/.env` for the Gemini API key and model name.
- If you prefer a deployed frontend, host the `frontend/` contents with any static site server.
