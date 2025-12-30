import os

class ScannerAgent:
    def __init__(self, target_dir):
        self.target_dir = target_dir

    def scan(self):
        """
        Walks through the target directory and finds all Markdown files.
        Returns a list of dictionaries containing file path and content.
        """
        print(f"--- Scanner: Starting scan in '{self.target_dir}' ---")
        
        found_files = []

        # os.walk is a generator that traverses directories
        for root, dirs, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    
                    # Read the content
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                        # Store structural data
                        file_data = {
                            "path": full_path,
                            "content": content
                        }
                        found_files.append(file_data)
                        print(f"✓ Found: {file}")
                        
                    except Exception as e:
                        print(f"x Error reading {file}: {e}")

        print(f"--- Scanner: Scan complete. Found {len(found_files)} files. ---")
        return found_files