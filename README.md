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
pip install -r requirements.txt, use UV command by Astral.sh instead of this 
cp .env.example .env
python run.py

## Status
In active development

## Deployment

### Backend (Render)
1. Connect GitHub repo to Render
2. Set root directory to `backend`
3. Add environment variables
4. Deploy!

### Frontend (Vercel)
1. Connect GitHub repo to Vercel
2. Set root directory to `frontend`
3. Add NEXT_PUBLIC_API_URL
4. Deploy!

## Deployment

### Backend (Render)
1. Connect GitHub repo to Render
2. Set root directory to `backend`
3. Add environment variables
4. Deploy!

### Frontend (Vercel)
1. Connect GitHub repo to Vercel
2. Set root directory to `frontend`
3. Add NEXT_PUBLIC_API_URL
4. Deploy!

## Deployment

### Backend (Render)
1. Connect GitHub repo to Render
2. Set root directory to `backend`
3. Add environment variables
4. Deploy!

### Frontend (Vercel)
1. Connect GitHub repo to Vercel
2. Set root directory to `frontend`
3. Add NEXT_PUBLIC_API_URL
4. Deploy!

## Project Structure

\`\`\`
code-review-agent/
├── backend/
│   ├── src/
│   │   ├── agents/          # AI agents
│   │   ├── api/             # FastAPI routes
│   │   ├── auth/            # GitHub OAuth
│   │   ├── db/              # Database models
│   │   ├── middleware/      # Rate limiting
│   │   ├── observability/   # Tracing & metrics
│   │   ├── security/        # Guardrails
│   │   └── utils/           # Helpers
│   └── tests/               # 20+ tests
└── frontend/
    ├── pages/               # Next.js pages
    ├── components/          # Reusable components
    └── styles/              # Global CSS
\`\`\`

## Project Structure

\`\`\`
code-review-agent/
├── backend/
│   ├── src/
│   │   ├── agents/          # AI agents
│   │   ├── api/             # FastAPI routes
│   │   ├── auth/            # GitHub OAuth
│   │   ├── db/              # Database models
│   │   ├── middleware/      # Rate limiting
│   │   ├── observability/   # Tracing & metrics
│   │   ├── security/        # Guardrails
│   │   └── utils/           # Helpers
│   └── tests/               # 20+ tests
└── frontend/
    ├── pages/               # Next.js pages
    ├── components/          # Reusable components
    └── styles/              # Global CSS
\`\`\`
