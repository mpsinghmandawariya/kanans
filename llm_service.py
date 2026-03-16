import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv('LLM_API_KEY', '')
        self.api_url = os.getenv('LLM_API_URL', 'https://api.groq.com/openai/v1/chat/completions')
        self.model = os.getenv('LLM_MODEL', 'llama-3.1-8b-instant')
        
    def call_llm(self, system_prompt, user_message, context=""):
        if not self.api_key:
            return "Error: LLM API key not configured. Please set LLM_API_KEY in .env file."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        if context:
            messages.append({
                "role": "system", 
                "content": f"Here is relevant information from the knowledge base to help answer the question:\n\n{context}"
            })
        
        messages.append({"role": "user", "content": user_message})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1024
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            elif response.status_code == 401:
                return "Error: Invalid API key. Please check your LLM_API_KEY in .env file."
            elif response.status_code == 429:
                return "Error: Rate limit exceeded. Please try again later."
            else:
                return f"Error: API request failed with status {response.status_code}. Please check your API configuration."
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "Error: Unable to connect to the API. Please check your internet connection."
        except Exception as e:
            return f"Error: An unexpected error occurred: {str(e)}"

llm_service = LLMService()
