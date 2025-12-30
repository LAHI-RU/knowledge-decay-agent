import os
from src.scanner import ScannerAgent
from src.evaluator import EvaluatorAgent
from src.notifier import NotifierAgent

def run_agentic_system():
    print("\n🚀 STARTING INTERNAL KNOWLEDGE DECAY AGENT\n")

    # --- CONFIGURATION ---
    # We point the scanner at our mock folder for now.
    # In a real app, this might be your actual 'docs/' folder.
    TARGET_DIRECTORY = "mock_docs"
    
    # 1. INITIALIZE AGENTS
    print("--- [1] Initializing Agents ---")
    scanner = ScannerAgent(TARGET_DIRECTORY)
    evaluator = EvaluatorAgent()
    notifier = NotifierAgent()

    # 2. SCANNING PHASE
    print("\n--- [2] Scanner Agent Active ---")
    scanned_files = scanner.scan()
    
    if not scanned_files:
        print("No files found to analyze. Exiting.")
        return

    # 3. EVALUATION PHASE
    print("\n--- [3] Evaluator Agent Active (Thinking...) ---")
    stale_files = []

    for file in scanned_files:
        # Ask the Evaluator to judge the content
        analysis = evaluator.evaluate(file['path'], file['content'])
        
        # If the brain says STALE, we add it to our report list
        if analysis['status'] == 'STALE':
            stale_files.append({
                "path": file['path'],
                "reason": analysis['reason']
            })
            
    # 4. NOTIFICATION PHASE
    print("\n--- [4] Notifier Agent Active ---")
    notifier.notify(stale_files)
    
    print("✅ SYSTEM FINISHED")

if __name__ == "__main__":
    run_agentic_system()