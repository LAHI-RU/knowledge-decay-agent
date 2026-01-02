import os
import argparse  # <--- New Import
from src.scanner import ScannerAgent
from src.evaluator import EvaluatorAgent
from src.notifier import NotifierAgent

def run_agentic_system(target_directory):
    print("\n🚀 STARTING INTERNAL KNOWLEDGE DECAY AGENT")
    print(f"🎯 Target: {target_directory}\n")

    # Check if the folder actually exists before starting
    if not os.path.exists(target_directory):
        print(f"❌ Error: The directory '{target_directory}' does not exist.")
        return

    # 1. INITIALIZE AGENTS
    print("--- [1] Initializing Agents ---")
    scanner = ScannerAgent(target_directory)
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
        analysis = evaluator.evaluate(file['path'], file['content'])
        
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
    # --- ARGUMENT PARSING LOGIC ---
    parser = argparse.ArgumentParser(description="Scan documentation for knowledge decay.")
    
    # We define a flag '--target' (or '-t' for short)
    parser.add_argument(
        "-t", "--target", 
        type=str, 
        default="mock_docs", 
        help="The folder path to scan for documentation."
    )
    
    args = parser.parse_args()
    
    # We pass the user's choice into our main function
    run_agentic_system(args.target)