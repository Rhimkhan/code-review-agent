import os
import base64
import httpx
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class FileChange:
    filename: str
    status: str
    patch: Optional[str]
    additions: int
    deletions: int
    contents: Optional[str] = None


class GitHubTools:

    def __init__(self):
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise RuntimeError("GITHUB_TOKEN is not set")
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = "https://api.github.com"

    async def get_pr_files(self, repo: str, pr_number: int) -> List[FileChange]:
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(
                f"{self.base_url}/repos/{repo}/pulls/{pr_number}/files"
            )
            response.raise_for_status()
            files = []
            for f in response.json():
                content = None
                if f['status'] in ['added', 'modified'] and f.get('sha'):
                    content = await self._get_content(client, repo, f['filename'], f['sha'])
                files.append(FileChange(
                    filename=f['filename'],
                    status=f['status'],
                    patch=f.get('patch'),
                    additions=f['additions'],
                    deletions=f['deletions'],
                    contents=content
                ))
            return files

    async def _get_content(self, client, repo, path, ref) -> Optional[str]:
        try:
            response = await client.get(
                f"{self.base_url}/repos/{repo}/contents/{path}",
                params={'ref': ref}
            )
            response.raise_for_status()
            encoded = response.json().get('content', '')
            return base64.b64decode(encoded).decode('utf-8')
        except Exception:
            return None