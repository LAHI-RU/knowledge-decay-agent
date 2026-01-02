import os
from src.github_client import GitHubConnector

class ScannerAgent:
    def __init__(self, target):
        self.target = target
        # Determine mode based on input format (e.g., "owner/repo" vs "folder/path")
        self.is_github = "/" in target and not os.path.exists(target)
        
        if self.is_github:
            print(f"--- Scanner: Detected GitHub Repository '{target}' ---")
            self.gh_connector = GitHubConnector()
        else:
            print(f"--- Scanner: Detected Local Directory '{target}' ---")

    def scan(self):
        """
        Decides which scan method to use.
        """
        if self.is_github:
            return self._scan_github()
        else:
            return self._scan_local()

    def _scan_local(self):
        """
        The original local file scanning logic.
        """
        found_files = []
        for root, dirs, files in os.walk(self.target):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        found_files.append({"path": full_path, "content": content})
                        print(f"✓ Found (Local): {file}")
                    except Exception as e:
                        print(f"x Error reading {file}: {e}")
        return found_files

    def _scan_github(self):
        """
        The new logic to fetch files via API.
        """
        found_files = []
        try:
            # 1. Get the repository object
            repo = self.gh_connector.client.get_repo(self.target)
            
            # 2. Start at the root of the repo
            contents = repo.get_contents("")
            
            # 3. Iterate through files (Queue-based traversal)
            while contents:
                file_content = contents.pop(0)
                
                if file_content.type == "dir":
                    # If directory, get its contents and add to queue
                    contents.extend(repo.get_contents(file_content.path))
                
                elif file_content.path.endswith(".md"):
                    # If Markdown, decode the raw bytes to string
                    print(f"✓ Found (GitHub): {file_content.path}")
                    found_files.append({
                        "path": file_content.path,
                        "content": file_content.decoded_content.decode("utf-8")
                    })
                    
        except Exception as e:
            print(f"x GitHub Scan Error: {e}")
            
        return found_files