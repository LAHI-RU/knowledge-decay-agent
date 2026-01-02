import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

class GitHubConnector:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        
        if not self.token:
            raise ValueError("GitHub Token not found! Check your .env file.")

        # Initialize the connection
        self.client = Github(self.token)

    def verify_connection(self):
        """
        Simple smoke test to check if we can talk to GitHub.
        Returns the username of the token owner.
        """
        try:
            user = self.client.get_user()
            return user.login
        except Exception as e:
            print(f"GitHub Connection Failed: {e}")
            return None