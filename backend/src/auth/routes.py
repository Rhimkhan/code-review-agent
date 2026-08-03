from fastapi import APIRouter
import httpx, os

router = APIRouter()

@router.get('/auth/github/login')
async def github_login():
    client_id = os.getenv('GITHUB_CLIENT_ID')
    return {'url': f'https://github.com/login/oauth/authorize?client_id={client_id}&scope=repo'}

@router.get('/auth/github/callback')
async def github_callback(code: str):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            'https://github.com/login/oauth/access_token',
            data={
                'client_id': os.getenv('GITHUB_CLIENT_ID'),
                'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
                'code': code
            },
            headers={'Accept': 'application/json'}
        )
        access_token = token_resp.json().get('access_token')
        return {'access_token': access_token}
