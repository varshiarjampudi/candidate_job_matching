# Recruitment Intelligence AI

### AI-Based Candidate–Job Matching System

**Team:** ElevateX – Team 5

## 📌 Overview

Recruitment Intelligence AI is an AI-powered system that helps recruiters find suitable candidates for different job roles by analyzing resumes against job requirements.

The system combines **RAG, semantic search, deterministic skill matching, candidate ranking, and Groq LLM analysis**.

## 🎯 Objectives

- Automate resume analysis
- Match candidates with job requirements
- Rank candidates based on required skills
- Show matched and missing skills
- Provide resume-based candidate evidence
- Generate AI-powered recruitment analysis

## 🔄 System Workflow

```text
Job Description + Resumes
          ↓
    PDF Processing
          ↓
       Chunking
          ↓
     Embeddings
          ↓
       ChromaDB
          ↓
 Semantic Candidate Retrieval
          ↓
 Deterministic Skill Matching
          ↓
   Candidate Ranking
          ↓
   Candidate Evidence
          ↓
     Groq LLM Analysis
          ↓
      Streamlit UI

💼 Supported Roles
Data Analyst
Python Developer
Backend Developer
Machine Learning Engineer
Data Scientist 

🧠 Key Features
Resume Processing

Loads and processes candidate resume PDFs.

Semantic Retrieval

Uses:

sentence-transformers/all-MiniLM-L6-v2

to generate embeddings and retrieve relevant candidates using ChromaDB.

Skill Matching

Candidate match score is calculated using:

Match Score =
Matched Required Skills / Total Required Skills × 100

The system displays:

Match Score
Similarity Score
Matched Skills
Missing Skills
Candidate Ranking

Candidates are ranked using deterministic skill-based scoring.

Candidate Evidence

The system displays relevant information from resumes to help explain candidate suitability.

AI Recruitment Analysis

Groq LLM provides evidence-based recruitment analysis after candidate ranking.

Important: The deterministic scoring system controls ranking. The LLM is used for analysis and explanation and does not override the ranking.

🛠️ Technology Stack
Python
LlamaIndex
Sentence Transformers
ChromaDB
Groq LLM
PyPDF
Streamlit
Pytest
Git & GitHub

📁 Project Structure
Candidate_job_matching/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── config/
├── data/
│   ├── resumes/
│   └── job_description/
│
├── evaluation/
├── scripts/
├── src/
│   ├── chunking.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── job_description_loader.py
│   ├── prompts.py
│   ├── rag_pipeline.py
│   ├── resume_parser.py
│   ├── retriveal.py
│   ├── scoring.py
│   └── vector_store.py
│
└── tests/
    ├── conftest.py
    ├── test_chunking.py
    ├── test_rag.py
    ├── test_retrieval.py
    └── test_scoring.py


🚀 Installation

git clone https://github.com/sandhya8899/candidate_job_matching.git
cd candidate_job_matching
python -m venv venv

Activate Environment — Windows
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt

🔑 Environment Setup

Create a .env file:

GROQ_API_KEY=your_groq_api_key

Do not commit the .env file or API keys to GitHub.

▶️ Run the Application
streamlit run app.py

Open:

http://localhost:8501
🧪 Testing

Run:

pytest

Current result:

14 passed
📈 Current Status

The core implementation and working prototype are completed and tested.

Future enhancements may include hybrid search, advanced reranking, API serving, authentication, caching, monitoring, and production deployment.

👥 Team

ElevateX – Team 5

Project: Recruitment Intelligence AI
Purpose: AI-powered candidate–job matching and recruitment analysis.

🔗 Repository

https://github.com/sandhya8899/candidate_job_matching