from src.llm import LLMClient

class EvaluatorAgent:
    def __init__(self):
        # We inject the brain (LLMClient) into the evaluator
        self.brain = LLMClient()

    def evaluate(self, file_path, content):
        """
        Asks the LLM to analyze the document content.
        Returns a dictionary: {'status': 'STALE' or 'FRESH', 'reason': '...'}
        """
        print(f"--- Evaluator: Analyzing {file_path}... ---")

        # 1. Construct the Prompt
        # We give the AI a 'persona' and clear instructions.
        prompt = f"""
        You are a Technical Documentation Auditor.
        Analyze the following documentation snippet for signs of 'staleness' or 'knowledge decay'.

        SIGNS OF DECAY:
        - Mentions "legacy", "deprecated", "old version", "v1".
        - Dates older than 2022.
        - Instructions that seem uncertain or marked "TODO".

        DOCUMENT CONTENT:
        "{content}"

        INSTRUCTIONS:
        - You must answer in exactly two lines.
        - Line 1: Either the word "STALE" or "FRESH".
        - Line 2: A brief reason why.
        """

        # 2. Get response from LLM
        response = self.brain.get_completion(prompt)

        # 3. Defensive Parsing (Handle AI unreliability)
        if not response:
            return {"status": "UNKNOWN", "reason": "AI Error"}

        lines = response.split("\n")
        
        # Clean up the status (remove whitespace)
        status = lines[0].strip().upper()
        
        # specific check to ensure we only get valid statuses
        if "STALE" in status:
            final_status = "STALE"
        elif "FRESH" in status:
            final_status = "FRESH"
        else:
            final_status = "UNKNOWN"

        reason = lines[1] if len(lines) > 1 else "No reason provided."

        return {
            "status": final_status,
            "reason": reason
        }