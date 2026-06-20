# 🚀 CareerPilot AI

CareerPilot AI is a full-stack career guidance platform that helps job seekers evaluate their resumes against target job descriptions. The application analyzes uploaded PDF resumes, identifies skill gaps, generates personalized learning roadmaps, and provides interview preparation recommendations.

---

## 📌 Overview

Finding the right skills for a target role can be challenging. CareerPilot AI simplifies this process by comparing a candidate's resume with a job description and generating actionable insights to improve job readiness.

The platform helps users:

* Upload and analyze PDF resumes
* Identify existing and missing skills
* Understand skill match percentage
* Receive personalized learning recommendations
* Prepare with role-specific interview questions

---

## ✨ Features

### 📄 Resume Upload & Parsing

* Upload resumes in PDF format
* Extract resume content using PyMuPDF

### 🎯 Skill Analysis

* Detect technical and professional skills present in the resume
* Compare resume skills with job requirements

### 📊 Skill Gap Identification

* Highlight missing skills required for the target role
* Provide recommendations for improvement

### 📚 Learning Roadmap

* Generate structured learning paths
* Suggest areas to focus on for career growth

### 🎤 Interview Preparation

* Generate tailored interview questions
* Help candidates prepare for technical and behavioral interviews

### 🌐 Interactive Web Interface

* Simple and responsive user interface
* FastAPI-powered backend APIs
* Real-time analysis results

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* PyMuPDF
* Pydantic

### Frontend

* HTML
* CSS
* JavaScript

### Development Tools

* Git
* GitHub
* VS Code

---

## 📂 Project Structure

```text
careerpilot-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   └── core/
│   │
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/careerpilot-ai.git
cd careerpilot-ai
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Backend

```bash
uvicorn app.adapters.api.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## ▶️ Run Frontend

Open:

```text
frontend/index.html
```

Or use a local server:

```bash
python -m http.server 5500
```

Then visit:

```text
http://localhost:5500
```

---

## 📈 Sample Workflow

1. Upload a PDF resume.
2. Paste the target job description.
3. Click **Analyze Resume**.
4. View:

   * ATS Score
   * Skill Match Percentage
   * Missing Skills
   * Learning Roadmap
   * Interview Questions
   * Resume Suggestions

---

## 🎯 Future Enhancements

* AI-powered resume rewriting
* Cover letter generation
* Personalized career recommendations
* Multi-role analysis
* Dashboard analytics
* Cloud deployment

---

## 💡 Business Value

CareerPilot AI helps students, fresh graduates, and professionals understand how well their profiles align with target roles and provides actionable recommendations to improve employability.

---

## 👨‍💻 Author

**Patati Yasaswi**

* Data Science Graduate
* Python Developer
* AI & Data Analytics Enthusiast

LinkedIn: [www.linkedin.com/in/patati-yasaswi2](http://www.linkedin.com/in/patati-yasaswi2)

GitHub: https://github.com/PatatiYasaswi
