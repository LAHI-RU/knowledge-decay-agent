import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

class LLMClient:
    def __init__(self):
        # 1. Get the API Key safely
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # 2. Defensive Programming: Crash early if no key is found
        if not self.api_key:
            raise ValueError("API Key not found! Make sure .env is set correctly.")

        # 3. Initialize the official OpenAI connection
        self.client = OpenAI(api_key=self.api_key)

    def get_completion(self, prompt, model="gpt-4o-mini"):
        """
        Sends a prompt to the AI and returns the text response.
        Using 'gpt-4o-mini' because it is cheap and fast for testing.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            # Extract just the text content
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return None