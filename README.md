# 🤖 Code Review Agent

An AI-powered multi-agent system that reviews code for bugs, security vulnerabilities, and quality issues.

## Architecture
- SecurityAgent - Detects SQL injection, hardcoded secrets
- QualityAgent - AST-based code quality analysis
- AnalystAgent - Groq LLM deep code review
- Orchestrator - Coordinates all agents in parallel

## Tech Stack
- Python 3.11, FastAPI, Groq API
- SQLAlchemy, PostgreSQL
- Bandit security scanning
- Next.js frontend

## Setup
cd backend
python -m venv venv
pip install -r requirements.txt
cp .env.example .env
python run.py

## Status
In active development
