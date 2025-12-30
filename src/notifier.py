class NotifierAgent:
    def notify(self, stale_files):
        """
        Receives a list of stale file objects and generates a report.
        """
        if not stale_files:
            print("--- Notifier: No stale files to report. Good job! ---")
            return

        print("\n" + "="*40)
        print("🚨 KNOWLEDGE DECAY DETECTED 🚨")
        print("="*40)
        
        for file in stale_files:
            print(f"📄 File: {file['path']}")
            print(f"⚠️ Reason: {file['reason']}")
            print(f"👉 Recommended Action: update or archive this document.")
            print("-" * 20)
            
        print(f"Total Stale Files: {len(stale_files)}")
        print("="*40 + "\n")