# 🤖 Code Review Agent

An AI-powered multi-agent system that automatically reviews code for bugs, security vulnerabilities, and quality issues.

## 🏗️ Architecture

- **SecurityAgent** - Detects SQL injection, hardcoded secrets, vulnerabilities
- **QualityAgent** - AST-based code quality analysis
- **AnalystAgent** - Groq LLM (Llama3) deep code review
- **Orchestrator** - Coordinates all agents in parallel

## 🛠️ Tech Stack

- Python 3.11, FastAPI, Groq API
- SQLAlchemy, PostgreSQL
- Bandit (security scanning)
- Next.js (frontend)

## 🚀 Setup

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python run.py

## 📊 Status

🚧 In active development