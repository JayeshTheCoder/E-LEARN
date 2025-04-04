import os
import requests
from flask import jsonify

# LLM Class for OpenRouter API
class LLM:
    def __init__(self, model, base_url, api_key):
        """
        Initialize the LLM with the model, base URL, and API key.
        
        Args:
            model (str): The model to use (e.g., "openai/google/gemini-2.0-flash-exp:free").
            base_url (str): The base URL for the API (e.g., "https://openrouter.ai/api/v1").
            api_key (str): The API key for authentication.
        """
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key is required.")

    def chat_completion(self, messages):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"model": self.model, "messages": messages}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print("OpenRouter raw response:", response.text)  # Debug: see raw JSON
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in chat_completion: {e}")
            raise

# Initialize the LLM with a hardcoded API key
llm = LLM(
    model="google/gemini-2.5-pro-exp-03-25:free",
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  
)

def handle_chat(request):
    """
    Handle the chatbot functionality.
    """
    data = request.json
    user_message = data.get('message', '')
    print(f"Received message: {user_message}")  # Debugging

    try:
        # Create the conversation history
        messages = [
            {"role": "system", "content": "You are a course advisor for PersonaLearn. Provide concise information about courses, recommendations, and learning paths. Only answer education-related questions."},
            {"role": "user", "content": user_message}
        ]

        # Get response from your LLM
        print("Sending request to OpenRouter...")  # Debugging
        response = llm.chat_completion(messages)
        print("Received response from OpenRouter:", response)  # Debugging

        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error in chat route: {str(e)}")  # Debugging
        return jsonify({"reply": "Sorry, I'm having trouble answering that. Please try again later."})

# Add a testing mode for terminal input/output
if __name__ == "__main__":
    print("Chatbot Testing Mode")
    print("Type your message below and press Enter. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":    
            print("Exiting chatbot testing mode.")
            break

        # Create the conversation history
        messages = [
            {"role": "system", "content": "You are a course advisor for PersonaLearn. Provide concise information about courses, recommendations, and learning paths. Only answer education-related questions."},
            {"role": "user", "content": user_input}
        ]

        try:
            # Get response from your LLM
            response = llm.chat_completion(messages)
            reply = response['choices'][0]['message']['content']
            print(f"Chatbot: {reply}")
        except Exception as e:
            print(f"Error: {str(e)}")