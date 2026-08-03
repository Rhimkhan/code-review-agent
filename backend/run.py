import asyncio
from dotenv import load_dotenv
load_dotenv()

from src.agents.orchestrator import Orchestrator

async def test():
    orchestrator = Orchestrator()
    sample_code = """
def login(username, password):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    password = "admin123"
    return query
"""
    result = await orchestrator.review_code(sample_code, "auth.py")
    print(f"Total findings: {result['total_findings']}")
    print(f"Summary: {result['summary']}")
    for f in result['findings']:
        print(f"  [{f['severity']}] Line {f['line']}: {f['message']}")

asyncio.run(test())