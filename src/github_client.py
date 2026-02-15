import os
from github import Github, GithubException
from dotenv import load_dotenv

class GitHubClient:
    def __init__(self):
        load_dotenv()
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
        self.client = Github(token)
        self._validate_connection()
    
    def _validate_connection(self):
        try:
            self.user = self.client.get_user()
            self.user.login
        except GithubException as e:
            raise ConnectionError(f"Failed to connect to GitHub: {e}")
    
    def get_authenticated_user(self):
        return self.user.login
    
    def get_repo(self, repo_name):
        return self.client.get_repo(repo_name)
