# Contributing to Code Review Agent

## Setup
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Install deps: `pip install -r requirements.txt`
4. Add `.env` with your keys
5. Run: `uvicorn src.api.server:app --reload`

## Running Tests
cd backend
pytest tests/ -v

## Adding a New Agent
1. Create `src/agents/your_agent.py`
2. Extend `BaseAgent`
3. Implement `analyze()` method
4. Register in `Orchestrator`
